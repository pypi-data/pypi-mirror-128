import traceback
import pprint
import logging
import os
import argparse
import random
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim

from tl2.proj.fvcore.checkpoint import Checkpointer

from .ddp.ddp_utils import parser_local_rank, is_distributed


def init_seeds(seed=0,
               rank=0,
               # cuda_deterministic=True
               ):
  seed = seed + rank
  print(f"{rank}: seed={seed}")

  random.seed(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)

  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

  # if cuda_deterministic:
  #   torch.backends.cudnn.deterministic = True
  #   torch.backends.cudnn.benchmark = False
  # else:  # faster, less reproducible
  #   torch.backends.cudnn.deterministic = False
  #   torch.backends.cudnn.benchmark = True
  pass


def requires_grad(model, flag=True):
  for p in model.parameters():
    p.requires_grad = flag


def print_number_params(models_dict, logger=None, add_info=""):
  print()
  if logger is None:
    logger = logging.getLogger('tl')
  for label, model in models_dict.items():
    if model is None:
      # logger.info(f'Number of params in {label}:\t 0M')
      logger.info(f'{label + ":":<40} '
                  f"{'paras:'} {0:10.6f}M  {add_info}")
    else:
      num_params = sum([p.data.nelement() for p in model.parameters()]) / 1e6
      num_bufs = sum([p.data.nelement() for p in model.buffers()])

      logger.info(f'{label + ":":<40} '
                  f"{'paras:'} {num_params:10.6f}M"
                  f"{'':<1} bufs: {str(num_bufs)}M  {add_info}",
                  )

def save_models(save_dir,
                model_dict,
                info_msg=None,
                cfg=None,
                msg_mode='w'):
  os.makedirs(save_dir, exist_ok=True)
  for name, model in model_dict.items():
    if hasattr(model, 'state_dict'):
      # module and optim
      torch.save(model.state_dict(), f"{save_dir}/{name}.pth")
      if isinstance(model, nn.Module):
        torch.save(model, f"{save_dir}/{name}_model.pth")
    else:
      # dict
      torch.save(model, f"{save_dir}/{name}.pth")

  if info_msg is not None:
    with open(f"{save_dir}/0info.txt", msg_mode) as f:
      f.write(f"{info_msg}\n")

  if cfg is not None:
    cfg.dump_to_file_with_command(f"{save_dir}/config_command.yaml", cfg.tl_command)

  pass

def load_models(save_dir,
                model_dict,
                rank=0,
                **kwargs):
  logger = logging.getLogger('tl')
  logger.info(f"Loading models from {save_dir}\n"
              f"models: {model_dict.keys()}")

  map_location = lambda storage, loc: storage.cuda(rank)

  for name, model in model_dict.items():
    ckpt_path = f"{save_dir}/{name}.pth"
    if not os.path.exists(ckpt_path):
      logger.info(f"Do not exist, skip load {ckpt_path}!")
      continue
    # if isinstance(model, torch.nn.Module):
    #   model_ckpt = Checkpointer(model=model)
    #   model_ckpt.load_state_dict_from_file(ckpt_path)
    #   del model_ckpt
    #   torch.cuda.empty_cache()
    if hasattr(model, 'load_state_dict'):
      logger.info(f"Loading {name:<40}: load_state_dict")
      loaded_state = torch.load(ckpt_path, map_location=map_location)
      if isinstance(model, nn.Module):
        # ret = model.load_state_dict(loaded_state, strict=strict)
        # if not strict:
        #   logger.info("\nmissing_keys\n" + pprint.pformat(ret.missing_keys))
        #   logger.info("\nunexpected_keys\n" + pprint.pformat(ret.unexpected_keys))
        model_ckpt = Checkpointer(model=model)
        model_ckpt.load_state_dict(loaded_state)
        del model_ckpt
      elif isinstance(model, optim.Optimizer):
        try:
          ret = model.load_state_dict(loaded_state)
        except:
          logger.info(traceback.format_exc())
      else:
        ret = model.load_state_dict(loaded_state)
      del loaded_state
      torch.cuda.empty_cache()
    else:
      logger.info(f"Loading {name:<40}: update")
      loaded_state = torch.load(ckpt_path, map_location=map_location)
      model.update(loaded_state)
      del loaded_state
      torch.cuda.empty_cache()
  pass

def torch_load(model_path, rank):
  map_location = lambda storage, loc: storage.cuda(rank)
  loaded_model = torch.load(model_path, map_location=map_location)
  logging.getLogger('tl').info(f"Load model: {model_path}")
  return loaded_model


def set_optimizer_lr(optimizer, lr):
  for param_group in optimizer.param_groups:
    param_group['lr'] = lr
  pass







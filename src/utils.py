"""
Module Name: Utility Functions (Backend)
Author: Kenneth Leung
Last Modified: 19 Mar 2023
"""
import taipy as tp

def create_and_submit_pipeline(pipeline_cfg):
    pipeline = tp.create_pipeline(pipeline_cfg)
    tp.submit(pipeline)
    return pipeline
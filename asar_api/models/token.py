from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from ..config import (OUTPUT_DIR_NAME,
                      TOKENS_FILE_NAME,
                      JIEBA_DICT_NAME,
                      JIEBA_DIR_NAME)
from .file_basis import FileBasis


class Token(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         file_name=TOKENS_FILE_NAME,
                         object_schema=TokenObjectSchema)
        self.jieba_dir_path = prj_path.joinpath(OUTPUT_DIR_NAME, JIEBA_DIR_NAME)
        self.jieba_dict_file = self.jieba_dir_path.joinpath(JIEBA_DICT_NAME)
    
    def init(self) -> None:
        super().init()
        self.jieba_dir_path.mkdir(parents=True)

    def gen_jieba_dict(self) -> None:
        content = self.content
        with open(file=self.jieba_dict_file,
                  mode='w',
                  encoding="utf-8") as f:
            for token, v in content.items():
                frequency = v.get('frequency', '')
                f.write(f'{token} {frequency}\n')


class TokenObjectSchema(BaseModel):
    frequency: Optional[int]

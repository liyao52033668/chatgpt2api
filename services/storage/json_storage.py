from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from services.storage.base import StorageBackend


class JSONStorageBackend(StorageBackend):
    """本地 JSON 文件存储后端"""

    def __init__(self, file_path: Path, auth_keys_path: Path | None = None):
        self.file_path = file_path
        self.auth_keys_path = auth_keys_path or file_path.with_name("auth_keys.json")
        self.cpa_config_path = file_path.parent / "cpa_config.json"
        self.image_index_path = file_path.parent / "image_index.json"
        self.config_path = file_path.parent / "config.json"
        self.backup_state_path = file_path.parent / "backup_state.json"
        self.register_config_path = file_path.parent / "register.json"
        self.sub2api_config_path = file_path.parent / "sub2api_config.json"
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.auth_keys_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _load_json_list(file_path: Path) -> list[dict[str, Any]]:
        if not file_path.exists():
            return []
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, Exception):
            return []

    @staticmethod
    def _save_json_list(file_path: Path, items: list[dict[str, Any]]) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(
            json.dumps(items, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _load_json_object(file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            return {}
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, Exception):
            return {}

    @staticmethod
    def _save_json_object(file_path: Path, data: dict[str, Any]) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def load_accounts(self) -> list[dict[str, Any]]:
        """从 JSON 文件加载账号数据"""
        return self._load_json_list(self.file_path)

    def save_accounts(self, accounts: list[dict[str, Any]]) -> None:
        """保存账号数据到 JSON 文件"""
        self._save_json_list(self.file_path, accounts)

    def load_auth_keys(self) -> list[dict[str, Any]]:
        """从 JSON 文件加载鉴权密钥数据"""
        if not self.auth_keys_path.exists():
            return []
        try:
            data = json.loads(self.auth_keys_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, Exception):
            return []
        if isinstance(data, dict):
            data = data.get("items")
        return data if isinstance(data, list) else []

    def save_auth_keys(self, auth_keys: list[dict[str, Any]]) -> None:
        """保存鉴权密钥数据到 JSON 文件"""
        self.auth_keys_path.parent.mkdir(parents=True, exist_ok=True)
        self.auth_keys_path.write_text(
            json.dumps({"items": auth_keys}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def load_cpa_config(self) -> dict[str, Any]:
        """从 JSON 文件加载 CPA 配置"""
        return self._load_json_object(self.cpa_config_path)

    def save_cpa_config(self, config: dict[str, Any]) -> None:
        """保存 CPA 配置到 JSON 文件"""
        self._save_json_object(self.cpa_config_path, config)

    def load_image_index(self) -> dict[str, Any]:
        """从 JSON 文件加载图片索引"""
        return self._load_json_object(self.image_index_path)

    def save_image_index(self, index: dict[str, Any]) -> None:
        """保存图片索引到 JSON 文件"""
        self._save_json_object(self.image_index_path, index)

    def load_config(self) -> dict[str, Any]:
        """从 JSON 文件加载主配置"""
        return self._load_json_object(self.config_path)

    def save_config(self, config: dict[str, Any]) -> None:
        """保存主配置到 JSON 文件"""
        self._save_json_object(self.config_path, config)

    def load_backup_state(self) -> dict[str, Any]:
        """从 JSON 文件加载备份状态"""
        return self._load_json_object(self.backup_state_path)

    def save_backup_state(self, state: dict[str, Any]) -> None:
        """保存备份状态到 JSON 文件"""
        self._save_json_object(self.backup_state_path, state)

    def load_register_config(self) -> dict[str, Any]:
        """从 JSON 文件加载注册配置"""
        return self._load_json_object(self.register_config_path)

    def save_register_config(self, config: dict[str, Any]) -> None:
        """保存注册配置到 JSON 文件"""
        self._save_json_object(self.register_config_path, config)

    def load_sub2api_config(self) -> dict[str, Any]:
        """从 JSON 文件加载 Sub2API 配置"""
        return self._load_json_object(self.sub2api_config_path)

    def save_sub2api_config(self, config: dict[str, Any]) -> None:
        """保存 Sub2API 配置到 JSON 文件"""
        self._save_json_object(self.sub2api_config_path, config)

    def health_check(self) -> dict[str, Any]:
        """健康检查"""
        try:
            # 检查文件是否可读写
            if self.file_path.exists():
                self.file_path.read_text(encoding="utf-8")
            return {
                "status": "healthy",
                "backend": "json",
                "file_exists": self.file_path.exists(),
                "file_path": str(self.file_path),
                "auth_keys_file_exists": self.auth_keys_path.exists(),
                "auth_keys_file_path": str(self.auth_keys_path),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "json",
                "error": str(e),
            }

    def get_backend_info(self) -> dict[str, Any]:
        """获取存储后端信息"""
        return {
            "type": "json",
            "description": "本地 JSON 文件存储",
            "file_path": str(self.file_path),
            "file_exists": self.file_path.exists(),
            "auth_keys_file_path": str(self.auth_keys_path),
            "auth_keys_file_exists": self.auth_keys_path.exists(),
        }

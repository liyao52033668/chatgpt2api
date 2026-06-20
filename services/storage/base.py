from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class StorageBackend(ABC):
    """抽象存储后端基类"""

    @abstractmethod
    def load_accounts(self) -> list[dict[str, Any]]:
        """加载所有账号数据"""
        pass

    @abstractmethod
    def save_accounts(self, accounts: list[dict[str, Any]]) -> None:
        """保存所有账号数据"""
        pass

    @abstractmethod
    def load_auth_keys(self) -> list[dict[str, Any]]:
        """加载所有鉴权密钥数据"""
        pass

    @abstractmethod
    def save_auth_keys(self, auth_keys: list[dict[str, Any]]) -> None:
        """保存所有鉴权密钥数据"""
        pass

    @abstractmethod
    def load_cpa_config(self) -> dict[str, Any]:
        """加载 CPA 配置"""
        pass

    @abstractmethod
    def save_cpa_config(self, config: dict[str, Any]) -> None:
        """保存 CPA 配置"""
        pass

    @abstractmethod
    def load_image_index(self) -> dict[str, Any]:
        """加载图片索引（保持兼容性，实际不保存到数据库）"""
        pass

    @abstractmethod
    def save_image_index(self, index: dict[str, Any]) -> None:
        """保存图片索引（保持兼容性，实际不保存到数据库）"""
        pass

    @abstractmethod
    def load_config(self) -> dict[str, Any]:
        """加载主配置"""
        pass

    @abstractmethod
    def save_config(self, config: dict[str, Any]) -> None:
        """保存主配置"""
        pass

    @abstractmethod
    def load_backup_state(self) -> dict[str, Any]:
        """加载备份状态"""
        pass

    @abstractmethod
    def save_backup_state(self, state: dict[str, Any]) -> None:
        """保存备份状态"""
        pass

    @abstractmethod
    def load_register_config(self) -> dict[str, Any]:
        """加载注册配置"""
        pass

    @abstractmethod
    def save_register_config(self, config: dict[str, Any]) -> None:
        """保存注册配置"""
        pass

    @abstractmethod
    def load_sub2api_config(self) -> dict[str, Any]:
        """加载 Sub2API 配置"""
        pass

    @abstractmethod
    def save_sub2api_config(self, config: dict[str, Any]) -> None:
        """保存 Sub2API 配置"""
        pass

    def add_log(self, item: dict[str, Any]) -> None:
        """添加日志条目（默认不实现，由专门的日志服务处理）"""
        pass

    def list_logs(self, type: str = "", start_date: str = "", end_date: str = "", limit: int = 200) -> list[dict[str, Any]]:
        """查询日志条目（默认不实现，由专门的日志服务处理）"""
        return []

    def delete_logs(self, ids: list[str]) -> dict[str, int]:
        """删除日志条目（默认不实现，由专门的日志服务处理）"""
        return {"removed": 0}

    @abstractmethod
    def health_check(self) -> dict[str, Any]:
        """健康检查，返回存储后端状态"""
        pass

    @abstractmethod
    def get_backend_info(self) -> dict[str, Any]:
        """获取存储后端信息"""
        pass

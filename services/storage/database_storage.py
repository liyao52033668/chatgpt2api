from __future__ import annotations

import hashlib
import json
from typing import Any

from sqlalchemy import Column, String, Text, create_engine, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from services.storage.base import StorageBackend

Base = declarative_base()


class AccountModel(Base):
    """账号数据模型"""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    access_token = Column(Text, unique=True, nullable=False)
    access_token_hash = Column(String(32), unique=True, nullable=False, index=True)
    data = Column(Text, nullable=False)  # JSON 格式存储完整账号数据


class AuthKeyModel(Base):
    """鉴权密钥数据模型"""
    __tablename__ = "auth_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_id = Column(String(255), unique=True, nullable=False, index=True)
    data = Column(Text, nullable=False)


class ChatGPTConfigModel(Base):
    """主配置数据模型"""
    __tablename__ = "chatgpt_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False, index=True)
    data = Column(Text, nullable=False)


class ChatGPTBackupStateModel(Base):
    """备份状态数据模型"""
    __tablename__ = "chatgpt_backup_state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False, index=True)
    data = Column(Text, nullable=False)


class ChatGPTCPAConfigModel(Base):
    """CPA 配置数据模型"""
    __tablename__ = "chatgpt_cpa_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False, index=True)
    data = Column(Text, nullable=False)


class ChatGPTRegisterConfigModel(Base):
    """注册配置数据模型"""
    __tablename__ = "chatgpt_register_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False, index=True)
    data = Column(Text, nullable=False)


class ChatGPTSub2APIConfigModel(Base):
    """Sub2API 配置数据模型"""
    __tablename__ = "chatgpt_sub2api_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False, index=True)
    data = Column(Text, nullable=False)


class DatabaseStorageBackend(StorageBackend):
    """数据库存储后端（支持 SQLite、PostgreSQL、MySQL 等）"""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True,  # 自动检测连接是否有效
            pool_recycle=3600,   # 1小时回收连接
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def load_accounts(self) -> list[dict[str, Any]]:
        """从数据库加载账号数据"""
        session = self.Session()
        try:
            accounts = []
            for row in session.query(AccountModel).all():
                try:
                    account_data = json.loads(row.data)
                    if isinstance(account_data, dict):
                        accounts.append(account_data)
                except json.JSONDecodeError:
                    continue
            return accounts
        finally:
            session.close()

    def save_accounts(self, accounts: list[dict[str, Any]]) -> None:
        """保存账号数据到数据库"""
        self._save_rows(AccountModel, accounts, "access_token")

    def load_auth_keys(self) -> list[dict[str, Any]]:
        """从数据库加载鉴权密钥数据"""
        return self._load_rows(AuthKeyModel)

    def save_auth_keys(self, auth_keys: list[dict[str, Any]]) -> None:
        """保存鉴权密钥数据到数据库"""
        self._save_rows(AuthKeyModel, auth_keys, "id", "key_id")

    def load_cpa_config(self) -> dict[str, Any]:
        """从数据库加载 CPA 配置"""
        return self._load_kv_row(ChatGPTCPAConfigModel, "cpa_config")

    def save_cpa_config(self, config: dict[str, Any]) -> None:
        """保存 CPA 配置到数据库"""
        self._save_kv_row(ChatGPTCPAConfigModel, "cpa_config", config)

    def load_image_index(self) -> dict[str, Any]:
        """加载图片索引（保持兼容性，实际不保存到数据库）"""
        return {}

    def save_image_index(self, index: dict[str, Any]) -> None:
        """保存图片索引（保持兼容性，实际不保存到数据库）"""
        pass

    def load_config(self) -> dict[str, Any]:
        """从数据库加载主配置"""
        return self._load_kv_row(ChatGPTConfigModel, "config")

    def save_config(self, config: dict[str, Any]) -> None:
        """保存主配置到数据库"""
        self._save_kv_row(ChatGPTConfigModel, "config", config)

    def load_backup_state(self) -> dict[str, Any]:
        """从数据库加载备份状态"""
        return self._load_kv_row(ChatGPTBackupStateModel, "backup_state")

    def save_backup_state(self, state: dict[str, Any]) -> None:
        """保存备份状态到数据库"""
        self._save_kv_row(ChatGPTBackupStateModel, "backup_state", state)

    def load_register_config(self) -> dict[str, Any]:
        """从数据库加载注册配置"""
        return self._load_kv_row(ChatGPTRegisterConfigModel, "register_config")

    def save_register_config(self, config: dict[str, Any]) -> None:
        """保存注册配置到数据库"""
        self._save_kv_row(ChatGPTRegisterConfigModel, "register_config", config)

    def load_sub2api_config(self) -> dict[str, Any]:
        """从数据库加载 Sub2API 配置"""
        return self._load_kv_row(ChatGPTSub2APIConfigModel, "sub2api_config")

    def save_sub2api_config(self, config: dict[str, Any]) -> None:
        """保存 Sub2API 配置到数据库"""
        self._save_kv_row(ChatGPTSub2APIConfigModel, "sub2api_config", config)

    def _load_kv_row(self, model: type, key: str) -> dict[str, Any]:
        """加载键值对数据"""
        session = self.Session()
        try:
            row = session.query(model).filter(model.key == key).first()
            if row:
                try:
                    return json.loads(row.data)
                except json.JSONDecodeError:
                    return {}
            return {}
        finally:
            session.close()

    def _save_kv_row(self, model: type, key: str, data: dict[str, Any]) -> None:
        """保存键值对数据"""
        session = self.Session()
        try:
            session.query(model).filter(model.key == key).delete()
            session.add(model(key=key, data=json.dumps(data, ensure_ascii=False)))
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def _load_rows(self, model: type[AccountModel] | type[AuthKeyModel]) -> list[dict[str, Any]]:
        session = self.Session()
        try:
            items = []
            for row in session.query(model).all():
                try:
                    item_data = json.loads(row.data)
                    if isinstance(item_data, dict):
                        items.append(item_data)
                except json.JSONDecodeError:
                    continue
            return items
        finally:
            session.close()

    def _save_rows(
        self,
        model: type[AccountModel] | type[AuthKeyModel],
        items: list[dict[str, Any]],
        source_key: str,
        target_key: str | None = None,
    ) -> None:
        session = self.Session()
        try:
            session.query(model).delete()
            for item in items:
                if not isinstance(item, dict):
                    continue
                key_value = str(item.get(source_key) or "").strip()
                if not key_value:
                    continue
                if model == AccountModel:
                    token_hash = hashlib.md5(key_value.encode('utf-8')).hexdigest()
                    session.add(
                        model(
                            access_token=key_value,
                            access_token_hash=token_hash,
                            data=json.dumps(item, ensure_ascii=False),
                        )
                    )
                else:
                    session.add(
                        model(
                            **{target_key or source_key: key_value},
                            data=json.dumps(item, ensure_ascii=False),
                        )
                    )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def health_check(self) -> dict[str, Any]:
        """健康检查"""
        try:
            session = self.Session()
            try:
                # 尝试执行简单查询
                session.execute(text("SELECT 1"))
                count = session.query(AccountModel).count()
                auth_key_count = session.query(AuthKeyModel).count()
                return {
                    "status": "healthy",
                    "backend": "database",
                    "database_url": self._mask_password(self.database_url),
                    "account_count": count,
                    "auth_key_count": auth_key_count,
                }
            finally:
                session.close()
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "database",
                "error": str(e),
            }

    def get_backend_info(self) -> dict[str, Any]:
        """获取存储后端信息"""
        db_type = "unknown"
        if "sqlite" in self.database_url:
            db_type = "sqlite"
        elif "postgresql" in self.database_url or "postgres" in self.database_url:
            db_type = "postgresql"
        elif "mysql" in self.database_url:
            db_type = "mysql"
        
        return {
            "type": "database",
            "db_type": db_type,
            "description": f"数据库存储 ({db_type})",
            "database_url": self._mask_password(self.database_url),
        }

    @staticmethod
    def _mask_password(url: str) -> str:
        """隐藏数据库连接字符串中的密码"""
        if "://" not in url:
            return url
        try:
            protocol, rest = url.split("://", 1)
            if "@" in rest:
                credentials, host = rest.split("@", 1)
                if ":" in credentials:
                    username, _ = credentials.split(":", 1)
                    return f"{protocol}://{username}:****@{host}"
            return url
        except Exception:
            return url

#for sql alchemy
# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     published = Column(Boolean, default=True)


#sql model
from datetime import datetime
from sqlmodel import TIMESTAMP, Boolean, Column, SQLModel, Field, Relationship, text



class Post_new(SQLModel, table=True):
    __tablename__ = "post_new"
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str
    content: str
    published: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default=text('true'))
    )
    created_at: datetime | None = Field(
        default=None, 
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    ) 
    user_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")

    user: "Users" = Relationship(back_populates="posts")


class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime | None = Field(
        default=None, 
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    posts: list["Post_new"] = Relationship(back_populates="user")



class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    user_id: int = Field(foreign_key="users.id", primary_key=True, ondelete="CASCADE")
    post_id: int = Field(foreign_key="post_new.id", primary_key=True, ondelete="CASCADE")
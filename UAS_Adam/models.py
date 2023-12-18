from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Jeruk(Base):
    __tablename__ = 'data_jeruk'
    jenis_jeruk: Mapped[str] = mapped_column(primary_key=True)
    rasa: Mapped[int] = mapped_column()
    kandungan_gula: Mapped[int] = mapped_column()
    ukuran: Mapped[int] = mapped_column()
    harga: Mapped[int] = mapped_column()
    aroma: Mapped[int] = mapped_column()  
    
    def __repr__(self) -> str:
        return f"Jeruk(jenis_jeruk={self.jenis_jeruk!r}, harga={self.harga!r})"

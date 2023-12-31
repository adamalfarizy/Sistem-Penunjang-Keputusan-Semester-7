PGDMP  (                	    {         
   dataset_jeruk    16.0    16.0     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16397 
   dataset_jeruk    DATABASE     �   CREATE DATABASE dataset_jeruk WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Indonesia.1252';
    DROP DATABASE dataset_jeruk;
                postgres    false            �            1259    16411 
   data_jeruk    TABLE     �   CREATE TABLE public.data_jeruk (
    jenis_jeruk text,
    rasa text,
    kandungan_gula text,
    ukuran text,
    harga text
);
    DROP TABLE public.data_jeruk;
       public         heap    postgres    false            �            1259    16446    nilai_bobot_harga    TABLE     J   CREATE TABLE public.nilai_bobot_harga (
    harga text,
    nilai text
);
 %   DROP TABLE public.nilai_bobot_harga;
       public         heap    postgres    false            �            1259    16436    nilai_bobot_kandungan_gula    TABLE     \   CREATE TABLE public.nilai_bobot_kandungan_gula (
    kandungan_gula text,
    nilai text
);
 .   DROP TABLE public.nilai_bobot_kandungan_gula;
       public         heap    postgres    false            �            1259    16426    nilai_bobot_rasa    TABLE     H   CREATE TABLE public.nilai_bobot_rasa (
    rasa text,
    nilai text
);
 $   DROP TABLE public.nilai_bobot_rasa;
       public         heap    postgres    false            �            1259    16441    nilai_bobot_ukuran    TABLE     L   CREATE TABLE public.nilai_bobot_ukuran (
    ukuran text,
    nilai text
);
 &   DROP TABLE public.nilai_bobot_ukuran;
       public         heap    postgres    false            �          0    16411 
   data_jeruk 
   TABLE DATA           V   COPY public.data_jeruk (jenis_jeruk, rasa, kandungan_gula, ukuran, harga) FROM stdin;
    public          postgres    false    215   �       �          0    16446    nilai_bobot_harga 
   TABLE DATA           9   COPY public.nilai_bobot_harga (harga, nilai) FROM stdin;
    public          postgres    false    219   �
       �          0    16436    nilai_bobot_kandungan_gula 
   TABLE DATA           K   COPY public.nilai_bobot_kandungan_gula (kandungan_gula, nilai) FROM stdin;
    public          postgres    false    217   �
       �          0    16426    nilai_bobot_rasa 
   TABLE DATA           7   COPY public.nilai_bobot_rasa (rasa, nilai) FROM stdin;
    public          postgres    false    216   �
       �          0    16441    nilai_bobot_ukuran 
   TABLE DATA           ;   COPY public.nilai_bobot_ukuran (ukuran, nilai) FROM stdin;
    public          postgres    false    218           �   �   x���1�0�99'@�b�c,EL,��"�����	P�j2���ӗ�t����V�ɫ#�1�*l���fq6��ŋFԀ#�����k�j%l�%S[�̝���ႁk-�����!O`�k�t��X�~ADi�����}��%d��~�?G���j�t��Z      �   !   x��14 NC.0�kh�s�A�\1z\\\ wB�      �   (   x�J�KI��4�
NMI�K�4�
��KO��4����� ���      �   $   x�K,N��4�*NMO,�4��M��,�4����� x�G      �   &   x��NM���4�
NMI�K�4�rJ-N,�4����� �;�     
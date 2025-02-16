PGDMP  #    %                |         	   SER_Tyuiu    16.4    16.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16819 	   SER_Tyuiu    DATABASE        CREATE DATABASE "SER_Tyuiu" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "SER_Tyuiu";
                postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    16840 
   group_stud    TABLE     ]   CREATE TABLE public.group_stud (
    gr_id integer NOT NULL,
    stud_id integer NOT NULL
);
    DROP TABLE public.group_stud;
       public         heap    postgres    false    4            �            1259    16830    lesson    TABLE     �   CREATE TABLE public.lesson (
    id integer NOT NULL,
    cabinet character varying(30),
    start_time time without time zone,
    end_time time without time zone,
    group_id integer,
    w_day integer
);
    DROP TABLE public.lesson;
       public         heap    postgres    false    4            �            1259    16825    s_group    TABLE     h   CREATE TABLE public.s_group (
    id integer NOT NULL,
    group_name character varying(10) NOT NULL
);
    DROP TABLE public.s_group;
       public         heap    postgres    false    4            �            1259    16820    student    TABLE     �   CREATE TABLE public.student (
    id integer NOT NULL,
    name character varying(60) NOT NULL,
    student_tag character varying(32),
    coins integer NOT NULL
);
    DROP TABLE public.student;
       public         heap    postgres    false    4            �            1259    16855    w_days    TABLE     e   CREATE TABLE public.w_days (
    id integer NOT NULL,
    day_name character varying(15) NOT NULL
);
    DROP TABLE public.w_days;
       public         heap    postgres    false    4            �          0    16840 
   group_stud 
   TABLE DATA           4   COPY public.group_stud (gr_id, stud_id) FROM stdin;
    public          postgres    false    218   t       �          0    16830    lesson 
   TABLE DATA           T   COPY public.lesson (id, cabinet, start_time, end_time, group_id, w_day) FROM stdin;
    public          postgres    false    217   �       �          0    16825    s_group 
   TABLE DATA           1   COPY public.s_group (id, group_name) FROM stdin;
    public          postgres    false    216   �       �          0    16820    student 
   TABLE DATA           ?   COPY public.student (id, name, student_tag, coins) FROM stdin;
    public          postgres    false    215   �       �          0    16855    w_days 
   TABLE DATA           .   COPY public.w_days (id, day_name) FROM stdin;
    public          postgres    false    219   J       0           2606    16844    group_stud PK_S-g 
   CONSTRAINT     T   ALTER TABLE ONLY public.group_stud
    ADD CONSTRAINT "PK_S-g" PRIMARY KEY (gr_id);
 =   ALTER TABLE ONLY public.group_stud DROP CONSTRAINT "PK_S-g";
       public            postgres    false    218            .           2606    16834    lesson lesson_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.lesson
    ADD CONSTRAINT lesson_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.lesson DROP CONSTRAINT lesson_pkey;
       public            postgres    false    217            ,           2606    16829    s_group s_group_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.s_group
    ADD CONSTRAINT s_group_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.s_group DROP CONSTRAINT s_group_pkey;
       public            postgres    false    216            *           2606    16824    student student_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.student DROP CONSTRAINT student_pkey;
       public            postgres    false    215            2           2606    16859    w_days w_days_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.w_days
    ADD CONSTRAINT w_days_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.w_days DROP CONSTRAINT w_days_pkey;
       public            postgres    false    219            5           2606    16845    group_stud FK_g-s_gr_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.group_stud
    ADD CONSTRAINT "FK_g-s_gr_id" FOREIGN KEY (gr_id) REFERENCES public.s_group(id) ON UPDATE CASCADE ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.group_stud DROP CONSTRAINT "FK_g-s_gr_id";
       public          postgres    false    216    218    4652            3           2606    16835    lesson FK_les_sgr    FK CONSTRAINT     �   ALTER TABLE ONLY public.lesson
    ADD CONSTRAINT "FK_les_sgr" FOREIGN KEY (group_id) REFERENCES public.s_group(id) ON UPDATE CASCADE ON DELETE SET NULL;
 =   ALTER TABLE ONLY public.lesson DROP CONSTRAINT "FK_les_sgr";
       public          postgres    false    217    4652    216            4           2606    16860    lesson FK_les_w-day    FK CONSTRAINT     �   ALTER TABLE ONLY public.lesson
    ADD CONSTRAINT "FK_les_w-day" FOREIGN KEY (w_day) REFERENCES public.w_days(id) ON UPDATE CASCADE ON DELETE RESTRICT NOT VALID;
 ?   ALTER TABLE ONLY public.lesson DROP CONSTRAINT "FK_les_w-day";
       public          postgres    false    217    4658    219            6           2606    16850    group_stud FK_s-g_stud_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.group_stud
    ADD CONSTRAINT "FK_s-g_stud_id" FOREIGN KEY (stud_id) REFERENCES public.student(id) ON UPDATE CASCADE ON DELETE CASCADE;
 E   ALTER TABLE ONLY public.group_stud DROP CONSTRAINT "FK_s-g_stud_id";
       public          postgres    false    215    218    4650            �      x�3�4�2�4�2��4�24�4����� $r�      �   /  x��VK��0]ۧ�%,h�>��g�8�v���#4B���+�oDUI��#��*��{eř�|A�������	F�:(
��6d��!㈒q��ly���Z�`��7k��6�(t�
Rgԥ���6�T��v�h3U�s�Ճ��`�J� z}*�˷�ܓ��cy.?���c@�����bƉ%w�X���5�e����d�p��ߌ�~@�cy��>K�֬V	u�Z�$��"	M,ua���·ި�H����M�U.ׇ�	N���ˣ4�>��:h�Ҍ��ra-��m���4�z��~�+V�U���ҺW{"+k�	�e���i�%��J��y�I��ms�����{*�n��o�D8�rY��*��J�?��T��#��Tޘ��1N�/-C��P���B�^S않R�ji3/��4���*��ET$Ñ�f���Y>�^�-X:_߶����m���r-f4���a����9�е5����ЦE#��Hm}{�����5�ލQ�ڑ��-�GB��{R	�׍������yL��Ư/�m�ׇm(nCiz{�����      �   �   x�-�;n�0D��ڏH�R�S�Ʒ��*���Gʀv��,G%��[aS>�SW�S+��*�a���d�2O��ȫBm��4�i�����"�*�M�&���ɞ�YD��a&�<*,�W6���ϼª����`��'�8I�
g�^��V�NJ����]��� f1cC3���� �Ɛ�[���?N�d�      �   |   x�3�,I-.	.M��tH�(J�JIM��4�2�ō��٩�&\Ɯf\�taÅ��]ؤ �( �^�q����� �3̑�Ѐ˄���[/6]l��q"���,
��ZR�R$39͸b���� q K�      �   �   x�-�I
BADםS����x���+Ap/��m;�K�^nd5H�T)^Ɖ���R~��Co��)�����4q��|�f���C��isq�(A��˱h�wE��m)��}��;E��V�3>�Mnl
uh둙� /�a(     
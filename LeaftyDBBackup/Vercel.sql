PGDMP                      |            verceldb    16.3    16.3 R    k           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            l           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            m           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            n           1262    16389    verceldb    DATABASE     j   CREATE DATABASE verceldb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE verceldb;
                default    false            o           0    0    DATABASE verceldb    ACL     2   GRANT ALL ON DATABASE verceldb TO neon_superuser;
                   default    false    3438            �            1259    32783    couriers    TABLE     u   CREATE TABLE public.couriers (
    "CourierID" integer NOT NULL,
    "CourierName" character varying(50) NOT NULL
);
    DROP TABLE public.couriers;
       public         heap    default    false            �            1259    32782    couriers_CourierID_seq    SEQUENCE     �   CREATE SEQUENCE public."couriers_CourierID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public."couriers_CourierID_seq";
       public          default    false    220            p           0    0    couriers_CourierID_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public."couriers_CourierID_seq" OWNED BY public.couriers."CourierID";
          public          default    false    219            �            1259    98393 
   dry_leaves    TABLE       CREATE TABLE public.dry_leaves (
    "DryLeavesID" integer NOT NULL,
    "UserID" character varying(36),
    "WetLeavesID" integer,
    "Processed_Weight" double precision,
    "Expiration" timestamp without time zone,
    "Status" character varying(50)
);
    DROP TABLE public.dry_leaves;
       public         heap    default    false            �            1259    98392    dry_leaves_DryLeavesID_seq    SEQUENCE     �   CREATE SEQUENCE public."dry_leaves_DryLeavesID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public."dry_leaves_DryLeavesID_seq";
       public          default    false    230            q           0    0    dry_leaves_DryLeavesID_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public."dry_leaves_DryLeavesID_seq" OWNED BY public.dry_leaves."DryLeavesID";
          public          default    false    229            �            1259    98351    flour    TABLE     �   CREATE TABLE public.flour (
    "FlourID" integer NOT NULL,
    "DryLeavesID" integer,
    "UserID" character varying(36),
    "Flour_Weight" double precision,
    "Expiration" timestamp without time zone,
    "Status" character varying(50)
);
    DROP TABLE public.flour;
       public         heap    default    false            �            1259    98350    flour_FlourID_seq    SEQUENCE     �   CREATE SEQUENCE public."flour_FlourID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public."flour_FlourID_seq";
       public          default    false    226            r           0    0    flour_FlourID_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public."flour_FlourID_seq" OWNED BY public.flour."FlourID";
          public          default    false    225            �            1259    32776 	   locations    TABLE     �   CREATE TABLE public.locations (
    "LocationID" integer NOT NULL,
    "LocationAddress" character varying(100),
    "Latitude" double precision NOT NULL,
    "Longitude" double precision NOT NULL
);
    DROP TABLE public.locations;
       public         heap    default    false            �            1259    32775    locations_LocationID_seq    SEQUENCE     �   CREATE SEQUENCE public."locations_LocationID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."locations_LocationID_seq";
       public          default    false    218            s           0    0    locations_LocationID_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."locations_LocationID_seq" OWNED BY public.locations."LocationID";
          public          default    false    217            �            1259    90112    otp    TABLE     �   CREATE TABLE public.otp (
    email character varying NOT NULL,
    otp_code character varying NOT NULL,
    expires_at timestamp without time zone NOT NULL
);
    DROP TABLE public.otp;
       public         heap    default    false            �            1259    32769    roles    TABLE     c   CREATE TABLE public.roles (
    "RoleID" integer NOT NULL,
    "RoleName" character varying(50)
);
    DROP TABLE public.roles;
       public         heap    default    false            �            1259    32768    roles_RoleID_seq    SEQUENCE     �   CREATE SEQUENCE public."roles_RoleID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."roles_RoleID_seq";
       public          default    false    216            t           0    0    roles_RoleID_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."roles_RoleID_seq" OWNED BY public.roles."RoleID";
          public          default    false    215            �            1259    49152    sessions    TABLE     �   CREATE TABLE public.sessions (
    session_id character varying(36) NOT NULL,
    user_id character varying(36),
    user_role integer,
    user_email character varying(36)
);
    DROP TABLE public.sessions;
       public         heap    default    false            �            1259    65644    shipment_flour    TABLE     V   CREATE TABLE public.shipment_flour (
    shipment_id integer,
    flour_id integer
);
 "   DROP TABLE public.shipment_flour;
       public         heap    default    false            �            1259    106513    shipment_flour_association    TABLE     b   CREATE TABLE public.shipment_flour_association (
    shipment_id integer,
    flour_id integer
);
 .   DROP TABLE public.shipment_flour_association;
       public         heap    default    false            �            1259    106497 	   shipments    TABLE     �  CREATE TABLE public.shipments (
    "ShipmentID" integer NOT NULL,
    "CourierID" integer,
    "UserID" character varying(36),
    "ShipmentQuantity" integer,
    "ShipmentDate" timestamp without time zone,
    "Check_in_Date" timestamp without time zone,
    "Check_in_Quantity" integer,
    "Harbor_Reception_File" boolean,
    "Rescalled_Weight" double precision,
    "Rescalled_Date" timestamp without time zone,
    "Centra_Reception_File" boolean
);
    DROP TABLE public.shipments;
       public         heap    default    false            �            1259    106496    shipments_ShipmentID_seq    SEQUENCE     �   CREATE SEQUENCE public."shipments_ShipmentID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."shipments_ShipmentID_seq";
       public          default    false    232            u           0    0    shipments_ShipmentID_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."shipments_ShipmentID_seq" OWNED BY public.shipments."ShipmentID";
          public          default    false    231            �            1259    32789    users    TABLE     �   CREATE TABLE public.users (
    "UserID" character varying(36) NOT NULL,
    "Username" character varying(50),
    "Email" character varying(100),
    "PhoneNumber" bigint,
    "Password" character varying(100),
    "RoleID" integer
);
    DROP TABLE public.users;
       public         heap    default    false            �            1259    98381 
   wet_leaves    TABLE       CREATE TABLE public.wet_leaves (
    "WetLeavesID" integer NOT NULL,
    "UserID" character varying(36),
    "Weight" double precision,
    "ReceivedTime" timestamp without time zone,
    "Expiration" timestamp without time zone,
    "Status" character varying(50)
);
    DROP TABLE public.wet_leaves;
       public         heap    default    false            �            1259    98380    wet_leaves_WetLeavesID_seq    SEQUENCE     �   CREATE SEQUENCE public."wet_leaves_WetLeavesID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public."wet_leaves_WetLeavesID_seq";
       public          default    false    228            v           0    0    wet_leaves_WetLeavesID_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public."wet_leaves_WetLeavesID_seq" OWNED BY public.wet_leaves."WetLeavesID";
          public          default    false    227            �           2604    32786    couriers CourierID    DEFAULT     |   ALTER TABLE ONLY public.couriers ALTER COLUMN "CourierID" SET DEFAULT nextval('public."couriers_CourierID_seq"'::regclass);
 C   ALTER TABLE public.couriers ALTER COLUMN "CourierID" DROP DEFAULT;
       public          default    false    220    219    220            �           2604    98396    dry_leaves DryLeavesID    DEFAULT     �   ALTER TABLE ONLY public.dry_leaves ALTER COLUMN "DryLeavesID" SET DEFAULT nextval('public."dry_leaves_DryLeavesID_seq"'::regclass);
 G   ALTER TABLE public.dry_leaves ALTER COLUMN "DryLeavesID" DROP DEFAULT;
       public          default    false    229    230    230            �           2604    98354    flour FlourID    DEFAULT     r   ALTER TABLE ONLY public.flour ALTER COLUMN "FlourID" SET DEFAULT nextval('public."flour_FlourID_seq"'::regclass);
 >   ALTER TABLE public.flour ALTER COLUMN "FlourID" DROP DEFAULT;
       public          default    false    225    226    226            �           2604    32779    locations LocationID    DEFAULT     �   ALTER TABLE ONLY public.locations ALTER COLUMN "LocationID" SET DEFAULT nextval('public."locations_LocationID_seq"'::regclass);
 E   ALTER TABLE public.locations ALTER COLUMN "LocationID" DROP DEFAULT;
       public          default    false    217    218    218            �           2604    32772    roles RoleID    DEFAULT     p   ALTER TABLE ONLY public.roles ALTER COLUMN "RoleID" SET DEFAULT nextval('public."roles_RoleID_seq"'::regclass);
 =   ALTER TABLE public.roles ALTER COLUMN "RoleID" DROP DEFAULT;
       public          default    false    216    215    216            �           2604    106500    shipments ShipmentID    DEFAULT     �   ALTER TABLE ONLY public.shipments ALTER COLUMN "ShipmentID" SET DEFAULT nextval('public."shipments_ShipmentID_seq"'::regclass);
 E   ALTER TABLE public.shipments ALTER COLUMN "ShipmentID" DROP DEFAULT;
       public          default    false    231    232    232            �           2604    98384    wet_leaves WetLeavesID    DEFAULT     �   ALTER TABLE ONLY public.wet_leaves ALTER COLUMN "WetLeavesID" SET DEFAULT nextval('public."wet_leaves_WetLeavesID_seq"'::regclass);
 G   ALTER TABLE public.wet_leaves ALTER COLUMN "WetLeavesID" DROP DEFAULT;
       public          default    false    228    227    228            [          0    32783    couriers 
   TABLE DATA           >   COPY public.couriers ("CourierID", "CourierName") FROM stdin;
    public          default    false    220   b       e          0    98393 
   dry_leaves 
   TABLE DATA           x   COPY public.dry_leaves ("DryLeavesID", "UserID", "WetLeavesID", "Processed_Weight", "Expiration", "Status") FROM stdin;
    public          default    false    230   Sb       a          0    98351    flour 
   TABLE DATA           k   COPY public.flour ("FlourID", "DryLeavesID", "UserID", "Flour_Weight", "Expiration", "Status") FROM stdin;
    public          default    false    226   �c       Y          0    32776 	   locations 
   TABLE DATA           ]   COPY public.locations ("LocationID", "LocationAddress", "Latitude", "Longitude") FROM stdin;
    public          default    false    218   !e       _          0    90112    otp 
   TABLE DATA           :   COPY public.otp (email, otp_code, expires_at) FROM stdin;
    public          default    false    224   >e       W          0    32769    roles 
   TABLE DATA           5   COPY public.roles ("RoleID", "RoleName") FROM stdin;
    public          default    false    216   �f       ]          0    49152    sessions 
   TABLE DATA           N   COPY public.sessions (session_id, user_id, user_role, user_email) FROM stdin;
    public          default    false    222   �f       ^          0    65644    shipment_flour 
   TABLE DATA           ?   COPY public.shipment_flour (shipment_id, flour_id) FROM stdin;
    public          default    false    223   �h       h          0    106513    shipment_flour_association 
   TABLE DATA           K   COPY public.shipment_flour_association (shipment_id, flour_id) FROM stdin;
    public          default    false    233   �h       g          0    106497 	   shipments 
   TABLE DATA           �   COPY public.shipments ("ShipmentID", "CourierID", "UserID", "ShipmentQuantity", "ShipmentDate", "Check_in_Date", "Check_in_Quantity", "Harbor_Reception_File", "Rescalled_Weight", "Rescalled_Date", "Centra_Reception_File") FROM stdin;
    public          default    false    232   �h       \          0    32789    users 
   TABLE DATA           c   COPY public.users ("UserID", "Username", "Email", "PhoneNumber", "Password", "RoleID") FROM stdin;
    public          default    false    221   �j       c          0    98381 
   wet_leaves 
   TABLE DATA           o   COPY public.wet_leaves ("WetLeavesID", "UserID", "Weight", "ReceivedTime", "Expiration", "Status") FROM stdin;
    public          default    false    228   �u       w           0    0    couriers_CourierID_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public."couriers_CourierID_seq"', 5, true);
          public          default    false    219            x           0    0    dry_leaves_DryLeavesID_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public."dry_leaves_DryLeavesID_seq"', 30, true);
          public          default    false    229            y           0    0    flour_FlourID_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public."flour_FlourID_seq"', 29, true);
          public          default    false    225            z           0    0    locations_LocationID_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."locations_LocationID_seq"', 1, false);
          public          default    false    217            {           0    0    roles_RoleID_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public."roles_RoleID_seq"', 6, true);
          public          default    false    215            |           0    0    shipments_ShipmentID_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."shipments_ShipmentID_seq"', 16, true);
          public          default    false    231            }           0    0    wet_leaves_WetLeavesID_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public."wet_leaves_WetLeavesID_seq"', 51, true);
          public          default    false    227            �           2606    32788    couriers couriers_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.couriers
    ADD CONSTRAINT couriers_pkey PRIMARY KEY ("CourierID");
 @   ALTER TABLE ONLY public.couriers DROP CONSTRAINT couriers_pkey;
       public            default    false    220            �           2606    98398    dry_leaves dry_leaves_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.dry_leaves
    ADD CONSTRAINT dry_leaves_pkey PRIMARY KEY ("DryLeavesID");
 D   ALTER TABLE ONLY public.dry_leaves DROP CONSTRAINT dry_leaves_pkey;
       public            default    false    230            �           2606    98356    flour flour_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.flour
    ADD CONSTRAINT flour_pkey PRIMARY KEY ("FlourID");
 :   ALTER TABLE ONLY public.flour DROP CONSTRAINT flour_pkey;
       public            default    false    226            �           2606    32781    locations locations_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY ("LocationID");
 B   ALTER TABLE ONLY public.locations DROP CONSTRAINT locations_pkey;
       public            default    false    218            �           2606    90118    otp otp_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY public.otp
    ADD CONSTRAINT otp_pkey PRIMARY KEY (email);
 6   ALTER TABLE ONLY public.otp DROP CONSTRAINT otp_pkey;
       public            default    false    224            �           2606    32774    roles roles_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY ("RoleID");
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public            default    false    216            �           2606    49156    sessions sessions_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (session_id);
 @   ALTER TABLE ONLY public.sessions DROP CONSTRAINT sessions_pkey;
       public            default    false    222            �           2606    106502    shipments shipments_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY ("ShipmentID");
 B   ALTER TABLE ONLY public.shipments DROP CONSTRAINT shipments_pkey;
       public            default    false    232            �           2606    32795    users users_Email_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.users
    ADD CONSTRAINT "users_Email_key" UNIQUE ("Email");
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT "users_Email_key";
       public            default    false    221            �           2606    32793    users users_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("UserID");
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            default    false    221            �           2606    98386    wet_leaves wet_leaves_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.wet_leaves
    ADD CONSTRAINT wet_leaves_pkey PRIMARY KEY ("WetLeavesID");
 D   ALTER TABLE ONLY public.wet_leaves DROP CONSTRAINT wet_leaves_pkey;
       public            default    false    228            �           1259    90119    ix_otp_email    INDEX     =   CREATE INDEX ix_otp_email ON public.otp USING btree (email);
     DROP INDEX public.ix_otp_email;
       public            default    false    224            �           2606    98399 !   dry_leaves dry_leaves_UserID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dry_leaves
    ADD CONSTRAINT "dry_leaves_UserID_fkey" FOREIGN KEY ("UserID") REFERENCES public.users("UserID");
 M   ALTER TABLE ONLY public.dry_leaves DROP CONSTRAINT "dry_leaves_UserID_fkey";
       public          default    false    221    3246    230            �           2606    98404 &   dry_leaves dry_leaves_WetLeavesID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dry_leaves
    ADD CONSTRAINT "dry_leaves_WetLeavesID_fkey" FOREIGN KEY ("WetLeavesID") REFERENCES public.wet_leaves("WetLeavesID");
 R   ALTER TABLE ONLY public.dry_leaves DROP CONSTRAINT "dry_leaves_WetLeavesID_fkey";
       public          default    false    228    230    3255            �           2606    98362    flour flour_UserID_fkey    FK CONSTRAINT        ALTER TABLE ONLY public.flour
    ADD CONSTRAINT "flour_UserID_fkey" FOREIGN KEY ("UserID") REFERENCES public.users("UserID");
 C   ALTER TABLE ONLY public.flour DROP CONSTRAINT "flour_UserID_fkey";
       public          default    false    3246    221    226            �           2606    49157    sessions sessions_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users("UserID");
 H   ALTER TABLE ONLY public.sessions DROP CONSTRAINT sessions_user_id_fkey;
       public          default    false    3246    221    222            �           2606    49162     sessions sessions_user_role_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_role_fkey FOREIGN KEY (user_role) REFERENCES public.roles("RoleID");
 J   ALTER TABLE ONLY public.sessions DROP CONSTRAINT sessions_user_role_fkey;
       public          default    false    3238    216    222            �           2606    106521 C   shipment_flour_association shipment_flour_association_flour_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.shipment_flour_association
    ADD CONSTRAINT shipment_flour_association_flour_id_fkey FOREIGN KEY (flour_id) REFERENCES public.flour("FlourID");
 m   ALTER TABLE ONLY public.shipment_flour_association DROP CONSTRAINT shipment_flour_association_flour_id_fkey;
       public          default    false    226    233    3253            �           2606    106516 F   shipment_flour_association shipment_flour_association_shipment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.shipment_flour_association
    ADD CONSTRAINT shipment_flour_association_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments("ShipmentID");
 p   ALTER TABLE ONLY public.shipment_flour_association DROP CONSTRAINT shipment_flour_association_shipment_id_fkey;
       public          default    false    233    3259    232            �           2606    106503 "   shipments shipments_CourierID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT "shipments_CourierID_fkey" FOREIGN KEY ("CourierID") REFERENCES public.couriers("CourierID");
 N   ALTER TABLE ONLY public.shipments DROP CONSTRAINT "shipments_CourierID_fkey";
       public          default    false    232    3242    220            �           2606    106508    shipments shipments_UserID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT "shipments_UserID_fkey" FOREIGN KEY ("UserID") REFERENCES public.users("UserID");
 K   ALTER TABLE ONLY public.shipments DROP CONSTRAINT "shipments_UserID_fkey";
       public          default    false    3246    232    221            �           2606    32796    users users_RoleID_fkey    FK CONSTRAINT        ALTER TABLE ONLY public.users
    ADD CONSTRAINT "users_RoleID_fkey" FOREIGN KEY ("RoleID") REFERENCES public.roles("RoleID");
 C   ALTER TABLE ONLY public.users DROP CONSTRAINT "users_RoleID_fkey";
       public          default    false    216    221    3238            �           2606    98387 !   wet_leaves wet_leaves_UserID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.wet_leaves
    ADD CONSTRAINT "wet_leaves_UserID_fkey" FOREIGN KEY ("UserID") REFERENCES public.users("UserID");
 M   ALTER TABLE ONLY public.wet_leaves DROP CONSTRAINT "wet_leaves_UserID_fkey";
       public          default    false    228    221    3246            )           826    16391     DEFAULT PRIVILEGES FOR SEQUENCES    DEFAULT ACL     {   ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;
          public          cloud_admin    false            (           826    16390    DEFAULT PRIVILEGES FOR TABLES    DEFAULT ACL     x   ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;
          public          cloud_admin    false            [   $   x�3�,J�J�2��tN-H,�2���s����� j��      e   [  x���IN�@�u�������7� l�ؠl@"H\��U�l���~�)�u�t9벭�.�*/�R�rY�k�ʵ�V��#���q&�Rz��������:1&�G�ڑ�0�y�u�Q*`w������ �{*Ցj %�=e�cV:(�9� e��*���՜ű��,0[��bjs�,,�#�,0��9�*K�S����F�'פ����b0�\�P�e[����ᛥ�,0�����՝�*�Y|u������#Ϥ]����p�~�����}���S=q�x(č����E�iۨt,�w� Sog.g�s��k�6lQ樻�%`]��E������}�}��ߦ��4M?ug��      a   S  x���=n1�뷧��f���r�)Ӱ�&�	"q�P��Y!Mi}z�|~M3�qm�<٠����'zw���4AH�bQW�I�D���~3��4h�~�_�IB%�����)K��pW��l,I�;���	y��Y����\�<ʥ��6��e��>\��e��bY�ib�%I�
吧Vĉt����T 7*���"���"�d�D�y/B��Q�Rҟ�z�<�O�A2��TF���*R~��Zdi�5�s�dL�r�~C�G+�Ce�X��d	�;Z9�m��ϧ��k��粒(���u�hl�k�W����h|'kR���@���B+2���i�o/�-      Y      x������ � �      _   :  x�e��n�@  �����e_�$P����Q��
�"���M�Ʀ�����e�MUf�q^�r��0NmN���b&�%�r���nV��*���SuR���|㸉�$Hb���F]�B�RCk;D�pG�����u���
�r�!���� ��.*�`y`���L�r�BԖ�QA��#��VG�K��b�ݨ�a��`����Y���޶ U��X�����Ķ����D6�_b��NUݹ���wM���	N~?���X�C�#��י��.�6\�w�t\���������	����P�8��+0�&�v�      W   G   x�3�tN�+)J�2��H,J�/�2�t��-H̫�2�tL����2��+K-�L�LM�2�J�JM.2c���� ~�      ]   �  x����n\1D��B��Wg�G>Dۀ���ƅ�>�"p��
	�̜�����Fa��$����c�XS�j��2hgr�J�(8��A���r�~����v�-ys�^"�Xl�m���P�F`���T�v��3p�m���Q*���0\�ReP�y�a��Q������kY���U[Хwm�mx��W%��`�JH�	C���$D:b��!4zI��䙉������O~�^̟��R�4Wc�|� >�6�3+:�X]M
Ԯi�����T��~�C޾o/�q||>����\	i�����d �����-Ǩkz�Z�tH�3l������}
�.M�u���R����a��ʿ@��6L�<=�R��wd]*{bB��y��>_��������~=\.�?�2�z      ^      x������ � �      h   F   x�ƹ�0 �Z7L`��.���nZk�Pe��z]n�3�y��V
.���V*n��]���Cټ��iv      g   y  x��TAr�0<ۯ�� �xD^�KӤ/�����tŇ�3:�`��"�Ox��^>d�]�WQ�]������>[k��YV�+��)��:��1ޢ���pHU��{��ƶ�4D�!nA��Dvy�nA
E<��΋�w}!����Bc\C	D�`�0T�_���C��8�Zha۰u���Tl:������]
�=1�`�'��9���R�n�y'<93i�\4+�y�eKpNV�s[f߇���}�k`��mд3qw(�{�r�iig��/w�+���gb͂����z@��Byz�=oYnn���(r	2(ڗ��"�F�?�Z���|ڂ�Y��ҽ�/��CהC*��v�W���5�Qƺ���<� �^/�      \   .  x��X�Rkɶ���AOK�7���s6ޤ,�!�_�r$�w�x!��{�\��z�������K�����}�a4��ns2_N�	��|����K�E�o��f��#���w���h�k;�ȇN:��G���2�-˫��|��'~^��|:�������)<=[	�t�y E�Ȩ�&����������q��'��e�3ߌ�ACrf�Mf�3?�.F��a�5�fJ��H
��b!):�S�\;V#}���Pƕ�x�8�A&⵶$ic�P������uҘ��t>��^:�s?���u�PY!9[G�߼8��e������[��g��:y�e�^����7w������a{~�<�#�.򤬡D�����I���\��X�k_O?�Eo�V��9�LJbst!Pa4�D��8\�2"�"s���F$�<r���ȳ���?��,]IQ#�V0 �7В�u�$��̍��j}�_I���+��٤7����H�K�mi
'.�L�HR�dm������q�s���rb���Y$2IA���h���D�j��j��~ [ʭ9�*��Ll��┒^�b>�wV��7�o�F#��9b�g�W0⹰$f�6)��k��/���ήK�հW���� �״d*p]j�U��d.�Z$��yCr��H%��B�"'.�����/��O�5X�ad��<fWqWDL�'A��a�E_װ�����n��1*)q/���RKd��JSmUc>|Γ^���Wk�÷��km�堩 �[����/z��5u"KGmc�i4x�-�F�d?�>�/�-���K�w��A�u�H��xJ#	 %�U���x�W���PW�+�,O��)����(I��*�hS���<��Ѳ~��;���Q�΀F�qΥB�V��&A�YZ���Z�X9Y��9ꯓyz�x_��� LN���i.2{��nt�x��Sd�r�'������ ������+�d,s�(ҏTQ�$*DAI�">g���G���n�A��e8=�~�<�fg�ǇS�H��7��xx�[i�M���i��rv�^L�u5�D���%C�uȄE���!8��F�P/��p�g]?\�,8D�d�3DZ�:����3��	,ꨢ|/������|C�K�?��f�䱷=�gå����n?]l��݇^{�5ܚ>����՛��JscA

�h]_	�adf�!E�%�V����5�jK�t�\����F"�xA�U��pꃖ�i�c@��߿5�Ն#���NN�������w}�8;�=\7��ۺ�B�������)���A�駖o�A�c�=�vD}�K�,�;�9�b�H���+�Fk��U�� �e4�kp{(è),
��h0��%<��o>փ�N�����{5��;�e�����B���e�5���Ů���ށ:��;����|8����iv`_((� <F���X;�d�(غ=?���t�Z�&1�Q�L%�Cn��'*Pg��ژ�������=5!W��(Q��EU���)��:�T#o�����g"�q�i��3�bL�+���x���E=�~"cv�5\�v)�������0����t���7��7�ߐ�j�#;�`�oŝ���o}~zpe��,�v�/۝ߓǗ{~qq�����jД�0���f5�V���܄f0��@��&� �5������ѽ?�2����Jgh�?�*2�$Ԟ�~����[�c�֙�}�;o��X�^��t7>�Oݻ�[�8�9�;4�M��K���a���E�-:��ie밷�ĺ5��B�m���ײ=Lawܝڣ��|��y�u�w�>k����7�ް,��:����J�b{��b�
t���l`KM��5��뼵�j?���3r!W�E�D�I��(X�ᐻ ���=?	�	h��v�Voa���
����l[�w��7���Ϟ���d��9?~
��,<�7�ux�7�gg�i�:l�BdYW�\ �R�p����q&��<�����:=*�l��r�W X`@���H�7��2ÂU��ٸR)�;[�|���s>����5��}�Ϻ��{:~�{{7;~����;��y�(�����HE��R�qJ�O�O��YoZi4�o<-�d���F�UA"�D����� `9�Q� �TTlD�`p�Z��usW7�ݿ�ڻ��s}T��6ϭGv5�����>�n�z��zs֙��������#���j���[Ox�F,�И.`�ᝓ_%�U�nkݒ��T�9�P������9�悪�A��WEtj���l6yjE��m�XB�%��B*���ޮa�z?}���!5�_�B0��c�,�$�
Ʋ�Y�ީA�7�5H�Ѵ����!�e&�,	<Qc4Vi�yMҮo`��? W{^�l�5���a&���2��Q����?1�j���5И�!V�W1���eC���X�E��t��� �k�v٤j^e��~�3<���S��)����n?�g[�\DߐX�.e�2r,H����K���˧v�'����`ev�m�BE��3B�{�9�-_�?�A�@�wX4��x�L�]K}r�(,�B���J�I;���3�xG�|5t���Ų���k���=��/~��͉�?�MZf�1�Q�S,����c���4��������SyM'�0���w�b;�s���яz�>�;���*� 5�VU�Q�����!��|2��F׶�ڐ}z��mw|~�z�*����Vs>�{��SҬ��`���^n*������b�P��@���Vp���Bѐh� 5�-���o�]j�_��X�0?�\������5���b>�[������ۿ��n.v���˃�Qkg:���inll�/x�ma      c     x�����1���)��dɖ���4�K��0��#�d�,����V*��+K�伃������$:�(Mv�<OpI��hf�C�O�&��S�hG�Kؽ������������G�� ���Y�q�� a# ��R��i �׸h�����@t��|���S`n���x�� �� vp�7 rHi�"]�8 � d� � lx����� �"R��17U4����?���F�SA	��WO��ik� )1W#�K� �xk�e7��)!w@����6~� ��6�1� �D�����'�gf�e�	��!������iY�z�9�P����~и���΀E�h�J� �B����������9�j	g���&>+O�t�4�q�${D0���q��(�`��������˧�<c� �QY�ج�\�vԺjS&��
1x�6=Fx*Ӻ�X!�M��r7�P����/o�����"6��
�U/`*����2�#c������0j����L�g}��\��u}�8Ȥ���g:� �������{V�uHuU�Z>��ðD(��:@�\��Ӫ��YbS�n����>]'�)������X�]_k��i���~/��)��"�=��'�/F��o, ��we/�幻_ݩ%8[�	�}�ä�`H���.?u���)h3Ī�����ȷ�A
$��Y��h�������kM߂E~�v����cاK�����ug�a�������y��[��y���$,̡V�m�?��~�����     
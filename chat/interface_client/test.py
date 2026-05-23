nome="f1l3n4m3c0d&Novo(a) Documento de Texto.txt3NDF1L3N4M3C0D&1044R¢H1V3L£Nb'ihsaduhsadoiusahd'3NDF1L3N4M3C0D&"
extract_file_name=nome.split("f1l3n4m3c0d&")
extract_file_name2=extract_file_name[1].split("3NDF1L3N4M3C0D&")
file_name=extract_file_name2[0]
extract_file_length=extract_file_name2[1].split("4R¢H1V3L£Nb")
file_length=int(extract_file_length[0])
file_bytes=extract_file_length[1]

client="f1l3n4m3c0d&Novo(a) Documento de Texto.txt3NDF1L3N4M3C0D&1044R¢H1V3L£Nb'ihsaduhsadoiusahd'3NDF1L3N4M3C0D&".encode()
servid="f1l3n4m3c0d&Novo(a) Documento de Texto.txt3NDF1L3N4M3C0D&1044R¢H1V3L£Nb'ihsaduhsadoiusahd'3NDF1L3N4M3C0D&"


print(len(servid))

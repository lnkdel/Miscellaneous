Echo off 
echo  �Զ���ȡIP��ַ....
netsh interface ip set address name = "��������" source = dhcp
echo  �Զ���ȡDNS������....
netsh interface ip set dns name = "��������" source = dhcp
Echo �Զ���ȡIP�ɹ�,����һ����,�Ϳ���ʹ�������ˡ���
Pause
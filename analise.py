import pandas as pd
import win32com.client as win32
import smtplib
import email.message

# importar a base de dados
tabela_vendas = pd.read_excel('C:/Users/danie/Downloads/Vendas (1).xlsx')

# visualizar a base de dados
pd.set_option('display.max_columns', None)
print(tabela_vendas)

# faturamento por loja
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)

# quantidade de produtos vendidos por loja
quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(quantidade)

print('-' * 50)
# ticket médio por produto em cada loja
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})
print(ticket_medio)

# enviar um email com o relatório
import smtplib
import email.message

def enviar_email():  
    corpo_email = f"""
   <p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{quantidade.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,</p>
<p>Lira</p>
'''
    """

    msg = email.message.Message()
    msg['Subject'] = "Analise"
    msg['From'] = 'danielvictorsaldanha@gmail.com'
    msg['To'] = 'danielvictorsaldanha@gmail.com'
    password = 'kzmerzdfbmlnkdyf' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')


# In[ ]:


enviar_email()
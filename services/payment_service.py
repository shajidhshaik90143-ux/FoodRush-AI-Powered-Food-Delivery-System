def process_payment(amount,method='cod'):
    return {'success':True,'amount':amount,'method':method,'transaction_id':'DEMO-'+str(int(amount*100))}

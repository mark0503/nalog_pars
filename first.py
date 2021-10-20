a = 'ru.vtb24.mobilebanking.protocol.product.SettlementCardAccountMto'
b = 'ru.vtb24.mobilebanking.protocol.product.SettlementAccountMto'
a = {
    'type': 'ru.vtb24.mobilebanking.protocol.product.SettlementAccount',
}
for i in a:
    if 'SettlementCardAccount' in a['type']:
        print('SettlementCardAccount')
    elif 'SettlementAccount' in a['type']:
        print('SettlementAccount')
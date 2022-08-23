from curses.ascii import isdigit
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

def validate_phone(string):
    if len(string) != 11:
        raise ValidationError("Enter a valid 11-digit phone number.")
    if string[0] != '1':
        raise ValidationError("Enter a valid phone number beginning with '1'.")
    for s in string:
        if not isdigit(s):
            raise ValidationError("There is a character in the phone number.")

def validate_digit(string):
    for s in string:
        if not isdigit(s):
            raise ValidationError("There is a non-digit character.")

class EUser(User):
    validate_phone = validate_phone
    # username, password, date_joined, email
    uid = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=20)
    phone = models.CharField(max_length=11, validators=[validate_phone])
    question1 = models.CharField(max_length=50)
    answer1 = models.CharField(max_length=50)
    question2 = models.CharField(max_length=50)
    answer2 = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.username

class Vendor(models.Model):
    validate_phone = validate_phone
    validate_digit = validate_digit
    vid = models.AutoField(primary_key=True)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)
    vname = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=6, validators=[validate_digit])
    country = models.CharField(max_length=10)
    language = models.CharField(max_length=10)
    glAcount = models.CharField(max_length=6)
    phone = models.CharField(max_length=11, validators=[validate_phone], blank=True, null=True)
    fax = models.CharField(max_length=10, validators=[validate_digit], blank=True, null=True)
    tpType = models.CharField(max_length=1, blank=True, null=True)
    companyCode = models.CharField(max_length=4)
    pOrg = models.CharField(max_length=4)
    currency = models.CharField(max_length=10, blank=True, null=True)
    score = models.IntegerField(default=100)

    def __str__(self) -> str:
        return self.vname + ', ' + self.city + ', ' + self.country

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    mname = models.CharField(max_length=5, unique=True)
    shortText = models.CharField(max_length=20, default='', blank=True)
    mType = models.CharField(max_length=5)
    mGroup = models.CharField(max_length=4)
    meaunit = models.CharField(max_length=3)
    netWeight = models.IntegerField(default=0)
    weightUnit = models.CharField(max_length=3)
    transGrp = models.CharField(max_length=1, blank=True, null=True)
    loadingGrp = models.CharField(max_length=1, blank=True, null=True)
    industrySector = models.CharField(max_length=1)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.mname

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4)
    client = models.CharField(max_length=20, default='MIDEA')
    companyCode = models.CharField(max_length=4)
    pOrg = models.CharField(max_length=4)
    pGrp = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.name

class MaterialItem(models.Model):
    id = models.AutoField(primary_key=True)
    sloc = models.CharField(max_length=4)
    sOrg = models.CharField(max_length=4)
    distrChannel = models.CharField(max_length=1, choices=[('I', 'IN'), ('W', 'WH')])
    unrestrictUse = models.IntegerField(default=0)
    blocked = models.IntegerField(default=0)
    qltyInspection = models.IntegerField(default=0)
    transit = models.IntegerField(default=0)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.material.mname + str(self.stock.id).zfill(4) + self.distrChannel

class StockHistory(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1, choices=[('1', 'In'), ('0', 'Out')])
    unrestrictUse = models.IntegerField(default=0)
    blocked = models.IntegerField(default=0)
    qltyInspection = models.IntegerField(default=0)
    item = models.ForeignKey(MaterialItem, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=False, auto_now=False)
    def __str__(self) -> str:
        return str(self.time) + ' ' + self.material.mname

class PurchaseRequisition(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, auto_now=False)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)

class RequisitionItem(models.Model):
    id = models.AutoField(primary_key=True)
    pr = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE)
    itemId = models.IntegerField()
    estimatedPrice = models.IntegerField()
    currency = models.CharField(max_length=10)
    quantity = models.IntegerField()
    deliveryDate = models.DateField()
    status = models.CharField(max_length=1, choices=[('0', 'Requisition Created'), ('1', 'Order Created')], default='0')
    meterial = models.ForeignKey(MaterialItem, on_delete=models.CASCADE)

class Quotation(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    deadline = models.DateField()
    deliveryDate = models.DateField()
    collNo = models.CharField(max_length=10)
    price = models.IntegerField(blank=True, null=True)
    currency = models.CharField(blank=True, null=True, max_length=10)
    validTime = models.DateField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, auto_now=False)
    rej = models.BooleanField(blank=True, null=True)
    ri = models.ForeignKey(RequisitionItem, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)

class PurchaseOrder(models.Model):
    validate_phone = validate_phone
    validate_digit = validate_digit
    id = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, validators=[validate_phone])
    fax = models.CharField(max_length=10, validators=[validate_digit])
    shippingAddress = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True, auto_now=False)
    rfq = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    itemId = models.IntegerField()
    quantity = models.IntegerField()
    deliveryDate = models.DateField()
    price = models.IntegerField()
    currency = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=1, choices=[('0', 'Not Deliveried'), ('1', 'Deliveried'), ('2', 'Invoice Received'), ('4', 'Payoff Completed')], default='0')
    qualityScore = models.IntegerField(blank=True, null=True)
    serviceScore = models.IntegerField(blank=True, null=True)
    quantityScore = models.IntegerField(blank=True, null=True)
    ontimeScore = models.IntegerField(blank=True, null=True)
    meterialItem = models.ForeignKey(MaterialItem, on_delete=models.CASCADE)

class GoodReceipt(models.Model):
    id = models.AutoField(primary_key=True)
    actualQnty = models.IntegerField()
    sType = models.CharField(max_length=1)
    time = models.DateField(auto_now_add=False, auto_now=False)
    postTime = models.DateField(auto_now_add=False, auto_now=False)
    orderItem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    fiscal = models.CharField(max_length=4)
    sumAmount = models.IntegerField()
    currency = models.CharField(max_length=10, blank=True, null=True)
    text = models.TextField(max_length=100, blank=True, null=True)
    invoiceDate = models.DateField()
    postDate = models.DateField()
    orderItem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    JEType = models.CharField(max_length=2)
    sumAmount = models.IntegerField()
    postDate = models.DateField()

class AccountDetail(models.Model):
    id = models.AutoField(primary_key=True)
    glAccount = models.CharField(max_length=6)
    type = models.CharField(max_length=1, choices=[('0', 'Credit'), ('1', 'Debt')])
    amount = models.IntegerField()
    gr = models.ForeignKey(GoodReceipt, on_delete=models.CASCADE, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
    je = models.ForeignKey(Account, on_delete=models.CASCADE)

class Record(models.Model):
    id = models.AutoField(primary_key=True)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)
    type = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True, auto_now=False)

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)
    type = models.IntegerField()

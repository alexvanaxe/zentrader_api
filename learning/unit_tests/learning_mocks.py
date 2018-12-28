import learning.models
import operation.models
import account.models
import datetime

def create_paper_buy_sell(cls, stock):
    cls.experience = operation.models.ExperienceData.objects.create(stock=stock,
                                                  account=account.models.Account.objects.all()[0],
                                                  creation_date=datetime.datetime.strptime('2017-06-30T15:52:30',
                                                                                  '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)


    cls.paper_buy = learning.models.PaperBuy.objects.create(stock=stock, account=account.models.Account.objects.all()[0],
                                             creation_date=datetime.datetime.strptime('2017-07-02T15:52:30',
                                                                             '%Y-%m-%dT%H:%M:%S'),
                                             amount=1000, price=30, experience=cls.experience)

    cls.paper_sell = learning.models.PaperSell.objects.create(stock=stock, account=account.models.Account.objects.all()[0],
                                             creation_date=datetime.datetime.strptime('2017-07-02T15:52:30',
                                                                             '%Y-%m-%dT%H:%M:%S'),
                                             amount=1000, price=30, stop_gain=34, stop_loss=27,
                                             paper_buy=cls.paper_buy)




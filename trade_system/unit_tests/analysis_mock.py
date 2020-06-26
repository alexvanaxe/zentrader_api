from trade_system.models import Analysis


def update_analysis(cls, operation):
    analysis = operation.analysis
    analysis.tunnel_top = 88
    analysis.tunnel_bottom = 72
    analysis.save()

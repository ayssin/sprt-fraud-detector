import numpy as np
import math

class SPRT:
    def __init__(self, alpha=0.01, beta=0.001, h0_mu=3.0, h0_sigma=1.0, h1_mu=5.0, h1_sigma=1.5):
        self.alpha = alpha
        self.beta = beta
        self.h0_mu = h0_mu
        self.h0_sigma = h0_sigma
        self.h1_mu = h1_mu
        self.h1_sigma = h1_sigma
        
        # Пороги Вальда
        self.A = math.log((1 - beta) / alpha)
        self.B = math.log(beta / (1 - alpha))
        
        # Состояние для каждого клиента
        self.log_lr = {}  # client_id -> current log_likelihood_ratio
        self.alerts = []  # список алертов (client_id, txn_id, log_lr)
    
    def log_likelihood_ratio(self, amount, is_fraud_hypothesis=True):
        """Вычисляет логарифм отношения правдоподобия для одной транзакции"""
        if is_fraud_hypothesis:
            mu = self.h1_mu
            sigma = self.h1_sigma
        else:
            mu = self.h0_mu
            sigma = self.h0_sigma
        
        # Логнормальное распределение
        log_amount = math.log(amount)
        ll = -math.log(amount * sigma * math.sqrt(2 * math.pi)) - ((log_amount - mu) ** 2) / (2 * sigma ** 2)
        return ll
    
    def update(self, client_id, amount, txn_id):
        """Обновляет статистику SPRT для клиента"""
        # Инициализация
        if client_id not in self.log_lr:
            self.log_lr[client_id] = 0.0
        
        # Логарифмы правдоподобия для H1 и H0
        ll_h1 = self.log_likelihood_ratio(amount, is_fraud_hypothesis=True)
        ll_h0 = self.log_likelihood_ratio(amount, is_fraud_hypothesis=False)
        
        # Обновление логарифма отношения правдоподобия
        self.log_lr[client_id] += (ll_h1 - ll_h0)
        
        # Проверка порогов
        if self.log_lr[client_id] >= self.A:
            # Алерт: мошенничество
            self.alerts.append({
                'client_id': client_id,
                'txn_id': txn_id,
                'log_lr': self.log_lr[client_id],
                'timestamp': None  # заполним позже
            })
            # Сброс статистики после алерта
            self.log_lr[client_id] = 0.0
            return 'FRAUD'
        elif self.log_lr[client_id] <= self.B:
            # Принимаем H0 (честный)
            self.log_lr[client_id] = 0.0
            return 'HONEST'
        else:
            return 'CONTINUE'
    
    def get_state(self, client_id):
        return self.log_lr.get(client_id, 0.0)
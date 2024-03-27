import datetime

class Result:
    def __init__(self, account_number, transaction_code, transaction_id, time, time_utc, timezone_name):
        self.account_number = account_number
        self.transaction_code = transaction_code
        self.transaction_id = transaction_id
        self.time = f"{time} ({timezone_name})"
        self.time_utc = time_utc

class Timezone:
    def __init__(self, name, offset_hour, offset_minutes):
        self.name = name
        self.offset_hour = offset_hour
        self.offset_minutes = offset_minutes

class Account:
    transaction_id = 0
    interest_rate = 0.1
    def __init__(self, account_number, first_name, last_name, preferred_time_zone, initial_balance=0):
        self.__account_number = account_number
        self.__first_name = first_name
        self.__last_name = last_name
        self.preferred_time_zone = preferred_time_zone
        self.__balance = initial_balance

    @property
    def first_name(self):
        return self.__first_name
    
    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name
    
    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def full_name(self):
        return f"{self.__first_name} {self.__last_name}"

    @property
    def balance(self):
        return self.__balance

    def confirmation_number(self, trans_type: str):
        time_utcnow = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        Account.transaction_id += 1
        return f"{trans_type}-{self.__account_number}-{time_utcnow}-{self.transaction_id}"

    def withdrawal(self, withdrawal_value):
        if withdrawal_value < 0:
            raise ValueError("Withdrawal amount can't be negative")
        if self.__balance - withdrawal_value < 0:
            declined_confirmation = self.confirmation_number("X")
            print(declined_confirmation)
            return
        else:
            self.__balance -= withdrawal_value
            withdrawal_confirmation = self.confirmation_number("W")
            print(withdrawal_confirmation)

    def deposit(self, deposit_value):
        if deposit_value < 0:
            raise ValueError("Deposit amount can't be negative")
        else:
            self.__balance += deposit_value
            deposit_confirmation = self.confirmation_number("D")
            print(deposit_confirmation)
    
    def deposit_interest(self):
        interest_amount = self.__balance * Account.interest_rate
        self.__balance += interest_amount
        interest_confirmation = self.confirmation_number("I")
        print(interest_confirmation)

    def parse_conf_number(self, conf_number: str, timezone):
        if isinstance(conf_number, str):
            parsed_num = conf_number.split("-")
            if len(parsed_num) != 4:
                raise ValueError("Wrong confirmation number syntax")
            real_time = datetime.datetime.strptime(parsed_num[2], "%Y%m%d%H%M%S")
            real_time += datetime.timedelta(hours=timezone.offset_hour, minutes=timezone.offset_minutes)
            utc_time = datetime.datetime.strptime(parsed_num[2], "%Y%m%d%H%M%S").strftime("%Y-%m-%dT%H:%M:%S")
            real_time_str = real_time.strftime("%Y-%m-%d %H:%M:%S")
            result = Result(parsed_num[1], parsed_num[0], parsed_num[3], real_time_str, utc_time, timezone.name)
            return result
        else:
            raise ValueError("Wrong confirmation number syntax")


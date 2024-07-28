import secrets

secret_key = secrets.token_hex(16)
print(secret_key)

#b0351af9384a13850c7c8570fa38f0cf

#app.config['SECRET_KEY'] = 'b0351af9384a13850c7c8570fa38f0cf'
#app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:/Users/Ch Naveen/Risk_Insights_Media/Dashboard_Project_Funding/users.db'
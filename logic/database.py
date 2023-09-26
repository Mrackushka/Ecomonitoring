import os
import pandas as pd

from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


class DB:
    def __init__(self):
        self.db_name = 'ecomonitoring.db'
        self.Base = declarative_base()
        self.Companies, self.Substances, self.CompaniesPollutions = self.create_tables()
        if not os.path.exists(self.db_name):
            self.engine = self.create_db()
            self.fill_db()
        else:
            self.engine = create_engine(f'sqlite:///{self.db_name}')
        self.session = sessionmaker(bind=self.engine)()

    def create_db(self):
        engine = create_engine(f'sqlite:///{self.db_name}')
        self.Base.metadata.create_all(engine)
        return engine

    def create_tables(self):
        class Companies(self.Base):
            __tablename__ = "companies"
            id = Column(Integer, primary_key=True)
            name = Column(String)
            activity_type = Column(String)
            ownership_form = Column(String)

        class Substances(self.Base):
            __tablename__ = "substances"
            id = Column(Integer, primary_key=True)
            name = Column(String)
            hazard_class = Column(String)
            mass_flow_rate = Column(Float)
            max_emissions = Column(Float)
            avg_daily_gdk = Column(Float)
            max_single_gdk = Column(Float)
            conc_limit_with_bg_clarke = Column(Float)
            toxicity_limit = Column(Float)
            oil_combussion_coeff = Column(Float)
            objects_waste_comb_coeff = Column(Float)
            forest_fires_comb_coeff = Column(Float)

        class CompaniesPollutions(self.Base):
            __tablename__ = "companies_pollutions"
            id = Column(Integer, primary_key=True)
            company_id = Column(Integer, ForeignKey("companies.id"))
            companies = relationship("Companies", backref="pollutions")
            substance_id = Column(Integer, ForeignKey("substances.id"))
            substances = relationship("Substances", backref="pollutions")
            emission_quantity = Column(Float)
            year = Column(Integer)

        return Companies, Substances, CompaniesPollutions

    def fill_db(self):
        companies_df = pd.read_csv('logic/csv/companies.csv')
        substances_df = pd.read_csv('logic/csv/substances.csv')
        companies_pollutions_df = pd.read_csv('logic/csv/companies_pollutions.csv')
        companies_df.to_sql('companies', self.engine, index=False, if_exists='replace')
        substances_df.to_sql('substances', self.engine, index=False, if_exists='replace')
        companies_pollutions_df.to_sql('companies_pollutions', self.engine, index=False, if_exists='replace')

    def get_companies_data(self):
        return self.session.query(self.Companies).all()

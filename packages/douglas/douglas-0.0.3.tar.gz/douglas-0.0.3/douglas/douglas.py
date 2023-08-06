from datetime import datetime as dt
import random
import numpy as np
import pandas as pd

surnames = pd.read_csv('https://raw.githubusercontent.com/Joevalencia/douglas/main/surnames.csv')
names = pd.read_csv('https://raw.githubusercontent.com/Joevalencia/douglas/main/babynames-clean.csv')

class NewDataset:
    def motor_dataset(self, number_of_insureds=10):
        n_insureds = number_of_insureds
        firstNames = names['John'].to_list()
        lastNames1 = surnames['name'].to_list()
        lastNames2 = surnames['name'].to_list()
        fuel = ['Gasoline', 'Diesel', 'Bio']

        # Common Brands
        vehicles0 = ['Fiat', 'Ford', 'Volkswagen', 'Toyota', 'Hyundai', 'Renault', 'Skoda']
        vehicles1 = ['Mercedes Benz', 'Audi', 'Chevrolet', 'Jeep', 'Maserati', 'Jaguar Cars']
        vehicles2 = ['Porsche', 'Aston Martin', 'Ferrari', 'Lamborghini', 'BMW']
        scaleMultiplier0, scaleMultiplier1, scaleMultiplier2 = 1, 2, 4

        # Year
        this_year = dt.now().year

        # Zone
        v0 = str([0, 1, 2, 3, 4, 5])

        # Marital Status
        marital = ['Single', 'Married', 'Widow']

        # Diet
        diet = ['omnivores', 'vegetarian', 'vegan']

        # Profession
        workers0 = ['plumber', 'painter', 'housekeeper', 'custodian', 'cleaning', 'maintenance', 'farmer',
                    'chef', 'cashier', 'chauffeur', 'maid', 'zoo caretaker', 'doorman', 'dishwasher']
        workers1 = ['mechanic', 'technician', 'driver', 'administrative', 'librarian', 'barman', 'logistic',
                    'agent', 'electrician', 'teacher', 'journalist', 'janitor', 'nurse']
        workers2 = ['actuary', 'doctor', 'researcher', 'accountant', 'analyst', 'financial advisor',
                    'engeener', 'physician', 'Anesthesiologist', 'comedian', 'surgeon', 'CEO']

        # El rango de edades entre las que queremos que estén las personas aseguradas
        yearEldest, yearYoungest = 1940, 2001

        # Los parámetros para la generación de valores del vehículo (Gamma)
        shape, scale = random.uniform(1, 1.5), 200000  # mean = shape*scale; var = shape*scale^2
        minVehicleValue = 10000

        # El rango de tasas para generar las primas
        minRate, maxRate = 0.02, 0.06

        auxForIndex = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789'

        insureds = pd.DataFrame()

        for i in range(n_insureds):
            index = ''
            for j in range(10):
                index = index + auxForIndex[random.randrange(len(auxForIndex))]
            insureds.loc[index, 'firstName'] = firstNames[random.randrange(len(firstNames))]
            insureds.loc[index, 'lastName1'] = lastNames1[random.randrange(len(lastNames1))]
            insureds.loc[index, 'lastName2'] = lastNames2[random.randrange(len(lastNames2))]
            insureds.loc[index, 'fuel'] = fuel[random.randrange(len(fuel))]
            insureds.loc[index, 'diet'] = diet[random.randrange(len(diet))]
            birthYear = int(random.randrange(yearEldest, yearYoungest))
            insureds.loc[index, 'age'] = this_year - birthYear
            vehicleType = np.random.binomial(2, .2)
            if vehicleType == 0:
                insureds.loc[index, 'vehicleType'] = vehicles0[random.randrange(len(vehicles0))]
                insureds.loc[index, 'Marital Status'] = marital[0]
                insureds.loc[index, 'job'] = workers0[random.randrange(len(workers0))]
                vehicleValue = np.floor(np.random.gamma(shape, scale * scaleMultiplier0))
            elif vehicleType == 1:
                insureds.loc[index, 'vehicleType'] = vehicles1[random.randrange(len(vehicles1))]
                insureds.loc[index, 'Marital Status'] = marital[1]
                insureds.loc[index, 'job'] = workers1[random.randrange(len(workers1))]
                vehicleValue = np.floor(np.random.gamma(shape, scale * scaleMultiplier1))
            else:
                insureds.loc[index, 'vehicleType'] = vehicles2[random.randrange(len(vehicles2))]
                insureds.loc[index, 'Marital Status'] = marital[2]
                insureds.loc[index, 'job'] = workers2[random.randrange(len(workers2))]
                vehicleValue = np.floor(np.random.gamma(shape, scale * scaleMultiplier2))
            insureds.loc[index, 'vehicleValue'] = vehicleValue
            insureds.loc[index, 'clm.incurred'] = (vehicleValue * random.uniform(minRate, maxRate)).round(2)

            insureds = insureds.reset_index()
            del insureds['index']
            vehicleZone = pd.Series(np.random.poisson(np.random.uniform(.7, 1), n_insureds))
            vehicleAge = pd.Series(np.random.randint(0, 11, n_insureds))
            claims = pd.Series(np.random.poisson(np.random.uniform(0.3, 1.3, n_insureds)))
            insureds['bmi'] = pd.Series(np.round(np.random.normal(23, 3, 10), 2), name='bmi')
            insureds['zone'], insureds['vehicleAge'] = vehicleZone, vehicleAge
            insureds['nbsin'] = claims
            insureds['exposure'] = pd.Series(np.round(np.random.uniform(0, 1, n_insureds), 4))
        return insureds
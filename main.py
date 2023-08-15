import json
import os
import uuid

file_name = 'werte.json'

def save_values(punkt_eingabe, linie_eingabe, polygon_eingabe, filename):

    if not os.path.exists(filename):
        data = {
            'Punkt': [{'id': str(uuid.uuid4()), 'coordinates': punkt_eingabe}] if punkt_eingabe else [],
            'Linie': [{'id': str(uuid.uuid4()), 'coordinates': linie_eingabe}] if linie_eingabe else [],
            'Polygon': [{'id': str(uuid.uuid4()), 'coordinates': polygon_eingabe}] if polygon_eingabe else []
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        with open(filename, 'r+') as f:
            data = json.load(f)
           
            if punkt_eingabe:
                if 'Punkt' not in data:
                    data['Punkt'] = []
                data['Punkt'].append({'id': str(uuid.uuid4()), 'coordinates': punkt_eingabe})
            if linie_eingabe:
                if 'Linie' not in data:
                    data['Linie'] = []
                data['Linie'].append({'id': str(uuid.uuid4()), 'coordinates': linie_eingabe})
            if polygon_eingabe:
                if 'Polygon' not in data:
                    data['Polygon'] = []
                data['Polygon'].append({'id': str(uuid.uuid4()), 'coordinates': polygon_eingabe})
    
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    

    
def load_values(shape_type, filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        if shape_type == 'Punkt':
            return [{'id': item['id'], 'coordinates': item['coordinates']} for item in data['Punkt']]
        elif shape_type == 'Linie':
            return [{'id': item['id'], 'coordinates': item['coordinates']} for item in data['Linie']]
        elif shape_type == 'Polygon':
            return [{'id': item['id'], 'coordinates': item['coordinates']} for item in data['Polygon']]
        else:
            return []


msg = '*Willkommen bei der Geometrien-Verwaltung!*'

def show_menu():
    print(msg)
    print('Sie können folgende Befehle verwenden:')
    print('1.eine Geometrie hinzufügen: insert-geom')
    print('2.eine Geometrie löschen: delete-geom')
    print('3.eine Liste von den Punkten anzeigen: points-list')
    print('4.eine Liste von den Punkten anzeigen: lines-list')
    print('5.eine Liste von den Punkten anzeigen: polygons-list')

def user_choice():
    choice = input('Geben Sie die Nummer Ihrer Wahl ein ')
    return choice

def geom_menu():
    print('Bitte wählen Sie den Geometrie-Type:')
    print('1. Punkt')
    print('2. Linie')
    print('3. Polygon')

def delete_menu():
    shape_types = {
        '1': 'Punkt',
        '2': 'Linie',
        '3': 'Polygon'
    }
    print('Bitte wählen Sie den Geometrie-Type, der gelöscht werden soll:')
    for key, value in shape_types.items():
        print(f'{key}. {value}')
    shape_type = input()
    if shape_type in shape_types:
        delete_choice(shape_types[shape_type])

def delete_choice(shape_type):
    with open(file_name, 'r') as f:
        data = json.load(f)
        if shape_type in data and data[shape_type]:
            print(f'Bitte geben Sie die ID des {shape_type}s ein, die Sie löschen möchten:')
            shape_id = input()
            delete_shape(shape_type, shape_id)
        else:
            print(f'Keine {shape_type} shape vorhanden')
            back()
        

def delete_shape(shape_type, shape_id):
    found = False
    with open(file_name, 'r+') as f:
        data = json.load(f)
        if shape_type in data:
            shapes = data[shape_type]
            for i, shape in enumerate(shapes):
                if shape['id'] == shape_id:
                    del shapes[i]
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                    print(f'Das {shape_type} mit der ID {shape_id} wurde gelöscht')
                    found = True
                    break
            if not found:
                print(f'Es gibt kein {shape_type} mit der ID {shape_id}')
                back()
        else:
            print(f'Keine Data vorhanden')
                      
                




punkt_koordinaten = []
linie_koordinaten = []
polygon_koordinaten = []

    
def get_Polygon_Koordinaten():
    if len(polygon_koordinaten) == 0:
        print('Es sind noch keine Koordinaten für Polygon angegeben')
    else:
        print(polygon_koordinaten)

def back():
    print('Drücken Sie "m" und dann die Eingabe-Taste, um zum Hauptmenü zurückzukehren')
    back_to_menu = input()
    if back_to_menu == 'm':
        main()
    else:
        print('Ungültige Eingabe. Bitte geben Sie m ein, um zum Hauptmenü zurückzukehren.')
        back()

def main():
    show_menu()
    choice = user_choice()


    if choice == '1':
        print('Sie haben Option 1 gewählt: insert-geom ')
        geom_menu()
        geom_choice = user_choice()

        if geom_choice == '1':
            print('Sie haben Option 1 gewählt: Punkt')
            while True:
                punkt_eingabe = input('Bitte geben Sie die Koordinaten des Punktes ein und bestätigen Sie mit der Eingabe-Taste: ')
                koordinaten = punkt_eingabe.split(',')
                if len(koordinaten) < 2:
                    print('Ungültige Eingabe. Bitte geben Sie zwei Koordinaten ein.')
                else:
                    x_str, y_str = koordinaten
                    x, y = int(x_str), int(y_str)
                    punkt_koordinaten.append([x, y])
                    punkt_koordinaten.sort(key=lambda x: x[0])
                    print('Koordinaten gespeichert:', punkt_koordinaten)
                    print('Benutzereingaben werden in Datei gespeichert.')
                    break
       
        elif geom_choice == '2':
            print('Sie haben Option 2 gewählt: Linie')
            while True:
                linie_eingabe = input('Bitte geben Sie die Koordinaten der Linie ein und bestätigen Sie mit der Eingabe-Taste: ')
                koordinaten = []

                for koordinate in linie_eingabe.split(';'):
                    koordinate = koordinate.strip()
                    if koordinate:
                        x_str, y_str = koordinate.split(',')
                        x, y = int(x_str), int(y_str)
                        koordinaten.append([x, y])
                        koordinaten.sort(key=lambda x: x[0])
    
                if len(koordinaten) < 2:
                    print('Bitte geben Sie mindestens 2 Koordinatenpaaren ein.')
                elif len(koordinaten) > 10:
                    print('Bitte geben Sie maximal 10 Koordinatenpaaren ein.')
                else:
                    linie_koordinaten.append(koordinaten)
                    print('Koordinaten gespeichert', linie_koordinaten)
                    print('Benutzereingaben werden in Datei gespeichert.')
                    break
            
        elif geom_choice == '3':
            print('Sie haben Option 3 gewählt: Polygon')
            while True:
                polygon_eingabe = input('Bitte geben Sie die Koordinaten des Polygons ein und bestätigen Sie mit der Eingabe-Taste: ')
                koordinaten = []

                for koordinate in polygon_eingabe.split(';'):
                    koordinate = koordinate.strip()
                    if koordinate:
                        x_str, y_str = koordinate.split(',')
                        x, y = int(x_str), int(y_str)
                        koordinaten.append([x, y])
                        koordinaten.sort(key=lambda x: x[0])

                if len(koordinaten) < 3:
                        print('Bitte geben Sie mindestens 3 Koordinatenpaaren ein.')
                elif len(koordinaten) > 20:
                    print('Bitte geben Sie maximal 20 Koordinatenpaaren ein.')
                else:
                    polygon_koordinaten.append(koordinaten)
                    break
            print('Koordinaten gespeichert', polygon_koordinaten)
            print('Benutzereingaben werden in Datei gespeichert.')
        else:
            print('Ungültige Auswahl. Bitte wählen Sie eine gültige Option aus.')  

    elif choice == '2':
        print('Sie haben Option 2 gewählt: delete-geom')
        delete_menu()

    elif choice == '3':
        # get all the punkten coordinates
        print('Sie haben Option 3 gewählt: points-list')
        punkten = load_values('Punkt', 'werte.json')
        if len(punkten) == 0:
            print('Es sind noch keine Koordinaten für Punkte angegeben')
            back()
        else:
            for punkt in punkten:
                print(f'ID: {punkt["id"]},\nKoordinaten: {punkt["coordinates"]}\n')
                back()
    elif choice == '4':
        # get all the linien coordinates
        print('Sie haben Option 4 gewählt: lines-list')
        linien = load_values('Linie', 'werte.json')
        if len(linien) == 0:
            print('Es sind noch keine Koordinaten für Linie angegeben')
            back()
        else:
            for linie in linien:
                print(f'ID: {linie["id"]},\nKoordinaten: {linie["coordinates"]}\n')
                back()
    elif choice == '5':
            # get all the polygons coordinates
            print('Sie haben Option 5 gewählt: polygons-list')
            polygons = load_values('Polygon', 'werte.json')
            if len(polygons) == 0:
                print('Es sind noch keine Koordinaten für Polygon angegeben')
                back()
            else:
                for polygon in polygons:
                    print(f'ID: {polygon["id"]},\nKoordinaten: {polygon["coordinates"]}\n')
                    back()
    else:
        print('Ungültige Auswahl. Bitte wählen Sie eine gültige Option aus.')    

    save_values(punkt_koordinaten, linie_koordinaten, polygon_koordinaten, 'werte.json')

if __name__ == '__main__':
    main()



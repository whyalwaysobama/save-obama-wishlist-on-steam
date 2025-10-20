import json
import os

class SaveProgress:
    def __init__(self):
        self.save_file = 'save_data.json'
        self.data = self.load_data()
    
    def load_data(self):
        """Carga los datos guardados o crea un archivo nuevo"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    return json.load(f)
            except:
                return self.create_default_data()
        else:
            return self.create_default_data()
    
    def create_default_data(self):
        """Crea datos por defecto para un nuevo juego"""
        return {
            'levels': {
                'tutorial': {'stars': 0, 'completed': False, 'best_time': None},
                1: {'stars': 0, 'completed': False, 'best_time': None},
                2: {'stars': 0, 'completed': False, 'best_time': None},
                3: {'stars': 0, 'completed': False, 'best_time': None},
                4: {'stars': 0, 'completed': False, 'best_time': None},
                5: {'stars': 0, 'completed': False, 'best_time': None},
                6: {'stars': 0, 'completed': False, 'best_time': None},
                7: {'stars': 0, 'completed': False, 'best_time': None},
                8: {'stars': 0, 'completed': False, 'best_time': None},
                9: {'stars': 0, 'completed': False, 'best_time': None},
                10: {'stars': 0, 'completed': False, 'best_time': None},
                11: {'stars': 0, 'completed': False, 'best_time': None},
            }
        }
    
    def save_data(self):
        """Guarda los datos en el archivo"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
    
    def update_level(self, level_id, stars_collected, time_taken, completed=False):
        """Actualiza los datos de un nivel"""
        # Convertir level_id a string para JSON
        level_key = str(level_id)
        
        if level_key not in self.data['levels']:
            self.data['levels'][level_key] = {'stars': 0, 'completed': False, 'best_time': None}
        
        # Actualizar estrellas (guardar el máximo)
        current_stars = self.data['levels'][level_key]['stars']
        self.data['levels'][level_key]['stars'] = max(current_stars, stars_collected)
        
        # Actualizar tiempo (guardar el mejor/menor tiempo)
        if time_taken is not None:
            current_best = self.data['levels'][level_key]['best_time']
            if current_best is None or time_taken < current_best:
                self.data['levels'][level_key]['best_time'] = round(time_taken, 2)
        
        # Marcar como completado
        if completed:
            self.data['levels'][level_key]['completed'] = True
        
        self.save_data()
    
    def get_level_stars(self, level_id):
        """Obtiene las estrellas de un nivel"""
        level_key = str(level_id)
        if level_key in self.data['levels']:
            return self.data['levels'][level_key]['stars']
        return 0
    
    def get_level_best_time(self, level_id):
        """Obtiene el mejor tiempo de un nivel"""
        level_key = str(level_id)
        if level_key in self.data['levels']:
            return self.data['levels'][level_key]['best_time']
        return None
    
    def is_level_completed(self, level_id):
        """Verifica si un nivel fue completado"""
        level_key = str(level_id)
        if level_key in self.data['levels']:
            return self.data['levels'][level_key]['completed']
        return False
    
    def get_total_stars(self):
        """Obtiene el total de estrellas recolectadas"""
        total = 0
        for level_data in self.data['levels'].values():
            total += level_data['stars']
        return total
    
    def reset_save(self):
        """Reinicia todos los datos guardados"""
        self.data = self.create_default_data()
        self.save_data()
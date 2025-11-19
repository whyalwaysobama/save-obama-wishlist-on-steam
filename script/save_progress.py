import json
import os

class SaveProgress:
    def __init__(self):
        self.saves_dir = 'saves'
        self.current_slot = None
        self.data = None
        
        # Crear directorio de saves si no existe
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
    
    def get_save_path(self, slot):
        """Obtiene la ruta del archivo de guardado para un slot"""
        return os.path.join(self.saves_dir, f'save_{slot}.json')
    
    def load_data(self, slot):
        """Carga los datos de un slot específico"""
        save_path = self.get_save_path(slot)
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r') as f:
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
                '1': {'stars': 0, 'completed': False, 'best_time': None},
                '2': {'stars': 0, 'completed': False, 'best_time': None},
                '3': {'stars': 0, 'completed': False, 'best_time': None},
                '4': {'stars': 0, 'completed': False, 'best_time': None},
                '5': {'stars': 0, 'completed': False, 'best_time': None},
                '6': {'stars': 0, 'completed': False, 'best_time': None},
                '7': {'stars': 0, 'completed': False, 'best_time': None},
                '8': {'stars': 0, 'completed': False, 'best_time': None},
                '9': {'stars': 0, 'completed': False, 'best_time': None},
                '10': {'stars': 0, 'completed': False, 'best_time': None},
                '11': {'stars': 0, 'completed': False, 'best_time': None},
            },
            'created_at': None,
            'last_played': None,
            'total_stars': 0
        }
    
    def save_data(self):
        """Guarda los datos en el archivo del slot actual"""
        if self.current_slot is None or self.data is None:
            return False
            
        try:
            save_path = self.get_save_path(self.current_slot)
            with open(save_path, 'w') as f:
                json.dump(self.data, f, indent=4)
            return True
        except Exception as e:
            return False
    
    def load(self, slot):
        """Carga un slot de guardado"""
        self.current_slot = slot
        self.data = self.load_data(slot)
        
        # Si es un save nuevo, inicializar timestamps
        if self.data.get('created_at') is None:
            import time
            self.data['created_at'] = time.time()
        
        import time
        self.data['last_played'] = time.time()
        self.save_data()
        return True
    
    def create(self, slot):
        """Crea un nuevo guardado en un slot"""
        self.current_slot = slot
        self.data = self.create_default_data()
        
        import time
        self.data['created_at'] = time.time()
        self.data['last_played'] = time.time()
        
        self.save_data()
        return True
    
    def save_exists(self, slot):
        """Verifica si existe un guardado en un slot"""
        return os.path.exists(self.get_save_path(slot))
    
    def get_save_info(self, slot):
        """Obtiene información de un slot sin cargarlo completamente"""
        if not self.save_exists(slot):
            return None
        
        try:
            save_path = self.get_save_path(slot)
            with open(save_path, 'r') as f:
                data = json.load(f)
            
            # Calcular estrellas totales
            total_stars = 0
            for level_data in data.get('levels', {}).values():
                total_stars += level_data.get('stars', 0)
            
            return {
                'slot': slot,
                'exists': True,
                'total_stars': total_stars,
                'created_at': data.get('created_at'),
                'last_played': data.get('last_played')
            }
        except:
            return None
    
    def list_saves(self):
        """Lista todos los guardados disponibles"""
        saves = []
        for slot in range(3):  # 3 slots: 0, 1, 2
            info = self.get_save_info(slot)
            if info:
                saves.append(info)
            else:
                saves.append({'slot': slot, 'exists': False})
        return saves
    
    def update_level(self, level_id, stars_collected, time_taken, completed=False):
        """Actualiza los datos de un nivel"""
        if self.data is None:
            return False
        
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
        
        # Actualizar timestamp
        import time
        self.data['last_played'] = time.time()
        
        self.save_data()
        return True
    
    def get_level_stars(self, level_id):
        """Obtiene las estrellas de un nivel"""
        if self.data is None:
            return 0
        
        level_key = str(level_id)
        if level_key in self.data['levels']:
            return self.data['levels'][level_key]['stars']
        return 0
    
    def get_level_best_time(self, level_id):
        """Obtiene el mejor tiempo de un nivel"""
        if self.data is None:
            return None
        
        level_key = str(level_id)
        if level_key in self.data['levels']:
            return self.data['levels'][level_key]['best_time']
        return None
    
    def is_level_completed(self, level_id):
        """Verifica si un nivel fue completado"""
        if self.data is None:
            return False
        
        level_key = str(level_id)
        if level_key in self.data['levels']:
            return self.data['levels'][level_key]['completed']
        return False
    
    def is_level_unlocked(self, level_id):
        """Verifica si un nivel está desbloqueado"""
        
        if level_id == 'tutorial' or level_id == 1:
            return True 
        
        if level_id == 11 :
            return self.get_total_stars() >= 30
        
        if self.data is None:
            return False
        
        prev_level = level_id - 1
        prev_level_key = str(prev_level)

        if prev_level_key in self.data['levels']:
            return self.data['levels'][prev_level_key]['completed']
        
        return False
    
    def get_total_stars(self):
        """Obtiene el total de estrellas recolectadas"""
        if self.data is None:
            return 0
        
        total = 0
        for level_data in self.data['levels'].values():
            total += level_data.get('stars', 0)
        return total
    
    def reset_current_save(self):
        """Reinicia el guardado actual"""
        if self.current_slot is not None:
            self.data = self.create_default_data()
            import time
            self.data['created_at'] = time.time()
            self.data['last_played'] = time.time()
            self.save_data()
    
    def delete_save(self, slot):
        """Elimina un guardado"""
        save_path = self.get_save_path(slot)
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
                return True
            except:
                return False
        return False
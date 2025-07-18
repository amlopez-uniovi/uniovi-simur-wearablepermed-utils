# Refactorización de Arquitectura CLI

## Cambios realizados en la arquitectura

### ✅ **Problema solucionado**
**Antes:** El código CLI estaba mezclado con la lógica de negocio en los módulos principales:
- `bin2csv.py` contenía función `run()` con argparse
- `file_management.py` contenía función `load_segment()` con argparse  
- `segmentation_cli.py` era el único módulo CLI dedicado

**Después:** Arquitectura limpia con separación de responsabilidades:
- Módulos principales: Solo lógica de negocio
- Módulos CLI dedicados: Solo lógica de interfaz de línea de comandos

### 🏗️ **Nueva arquitectura**

```
src/uniovi_simur_wearablepermed_utils/
├── bin2csv.py              # ✅ Solo lógica de negocio
├── file_management.py      # ✅ Solo lógica de negocio  
├── segmentation.py         # ✅ Solo lógica de negocio
├── bin2csv_cli.py          # ✅ CLI para bin2csv
├── file_management_cli.py  # ✅ CLI para file_management
└── segmentation_cli.py     # ✅ CLI para segmentation
```

### 📝 **setup.cfg actualizado**

```ini
console_scripts =
     sensor_bin_to_csv = uniovi_simur_wearablepermed_utils.bin2csv_cli:main
     csv_to_segmented_activity = uniovi_simur_wearablepermed_utils.file_management_cli:main
     segmented_activity_to_stack = uniovi_simur_wearablepermed_utils.segmentation_cli:main
```

**Patrón consistente:** Todos los comandos apuntan a `*_cli:main`

### 🔧 **Módulos CLI creados**

#### 1. `bin2csv_cli.py`
- Interfaz CLI para conversión BIN a CSV
- Validación de archivos, manejo de errores
- Opción verbose con información detallada

#### 2. `file_management_cli.py`  
- Interfaz CLI para segmentación de actividades
- Manejo de argumentos de plot/no-plot
- Validación de archivos CSV y Excel

#### 3. `segmentation_cli.py`
- Interfaz CLI para conversión a stack
- Parsing de columnas (slice o lista)
- Validación de ventanas y pasos

### 🧹 **Módulos principales limpiados**

#### `bin2csv.py`
- ❌ Eliminada función `run()`
- ✅ Solo función `bin2csv()` de negocio
- ✅ Mantiene CLI básico para uso standalone

#### `file_management.py`
- ❌ Eliminada función `load_segment()`
- ✅ Solo función `load_segment_wpm_data()` de negocio
- ✅ Módulo limpio y enfocado

#### `segmentation.py`
- ✅ Ya tenía arquitectura limpia
- ✅ Funciones de negocio separadas del CLI

### 🎯 **Ventajas de la nueva arquitectura**

1. **Separación clara de responsabilidades**
   - Módulos de negocio: Solo lógica de procesamiento
   - Módulos CLI: Solo interfaz de usuario

2. **Mantenibilidad mejorada**
   - Cambios en CLI no afectan lógica de negocio
   - Cambios en lógica no afectan CLI

3. **Testabilidad**
   - Fácil testear lógica de negocio sin CLI
   - Fácil testear CLI sin lógica compleja

4. **Consistencia**
   - Patrón uniforme para todos los comandos
   - Nomenclatura coherente

5. **Escalabilidad**
   - Fácil añadir nuevos comandos
   - Estructura clara para futuros desarrolladores

### 📋 **Comandos funcionando**

```bash
# Todos los comandos ahora usan módulos CLI dedicados
sensor_bin_to_csv --help         # ✅ bin2csv_cli:main
csv_to_segmented_activity --help # ✅ file_management_cli:main  
segmented_activity_to_stack --help # ✅ segmentation_cli:main
```

### 🔄 **Comparación antes/después**

| Comando | Antes | Después |
|---------|-------|---------|
| `sensor_bin_to_csv` | `bin2csv:run` | `bin2csv_cli:main` |
| `csv_to_segmented_activity` | `file_management:load_segment` | `file_management_cli:main` |
| `segmented_activity_to_stack` | `segmentation_cli:main` | `segmentation_cli:main` |

**Resultado:** Arquitectura uniforme, limpia y mantenible ✅

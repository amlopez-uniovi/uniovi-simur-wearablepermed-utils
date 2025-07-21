# Resumen de Refactorización de Scripts CLI

## Cambios realizados

### 1. Renombrado de scripts y comandos

**Nombres anteriores:**
- `convert_bin_to_csv.py` → `sensor_bin_to_csv.py`
- `csv2segmented_data.py` → `csv_to_segmented_activity.py`
- `segmented_data2stacked_data.py` → `segmented_activity_to_stack.py`

**Comandos globales:**
- `bin2csv` → `sensor_bin_to_csv`
- `csv2segmented_data` → `csv_to_segmented_activity`
- `segmented_data2stacked_data` → `segmented_activity_to_stack`

### 2. Nueva nomenclatura del pipeline

La nueva nomenclatura refleja mejor el flujo de procesamiento:

```
sensor_bin_to_csv → csv_to_segmented_activity → segmented_activity_to_stack → stack_to_features
```

### 🚀 Utilidad Interactiva

**`wpm_interactive_pipeline`** - Pipeline interactivo que guía paso a paso:
- Prompts interactivos con validación
- Configuración asistida de parámetros  
- Manejo de errores con opciones de reintentar
- Progreso visual y confirmaciones

## Comandos disponibles después del refactoring

### 🚀 Pipeline Interactivo (Recomendado)
- **wpm_interactive_pipeline**: Herramienta interactiva que guía paso a paso a través del pipeline completo

### Comandos Individuales
1. **sensor_bin_to_csv**: Convierte archivos BIN a CSV
2. **csv_to_segmented_activity**: Carga y segmenta datos desde CSV y actividades Excel
3. **segmented_activity_to_stack**: Combina y apila datos segmentados usando ventanas
4. **stack_to_features**: Extrae características de datos apilados y las guarda en NPZ

### 3. Archivos modificados

- `/scripts/sensor_bin_to_csv.py` - Renombrado y actualizado
- `/scripts/csv_to_segmented_activity.py` - Renombrado y actualizado
- `/scripts/segmented_activity_to_stack.py` - Renombrado y actualizado
- `/scripts/README.md` - Actualizado con nueva nomenclatura
- `/setup.cfg` - Actualizado console_scripts con nuevos nombres
- `/src/uniovi_simur_wearablepermed_utils/segmentation_cli.py` - Nuevo módulo CLI

### 4. Configuración actualizada

**setup.cfg:**
```ini
console_scripts =
     sensor_bin_to_csv = uniovi_simur_wearablepermed_utils.bin2csv_cli:main
     csv_to_segmented_activity = uniovi_simur_wearablepermed_utils.file_management_cli:main
     segmented_activity_to_stack = uniovi_simur_wearablepermed_utils.segmentation_cli:main
     stack_to_features = uniovi_simur_wearablepermed_utils.feature_extraction_cli:main
```

### 5. Uso después de la instalación

```bash
# Instalar en modo desarrollo
pip install -e .

# Usar comandos globalmente

# Pipeline interactivo (recomendado)
wpm_interactive_pipeline

# O comandos individuales
sensor_bin_to_csv input.BIN output.csv
csv_to_segmented_activity data.csv activities.xlsx Thigh
segmented_activity_to_stack file1.npz file2.npz --window-size 250 --output result.npz
stack_to_features result.npz --output features.npz

# O usar scripts directamente

# Pipeline interactivo
python scripts/wpm_interactive_pipeline.py

# Scripts individuales
python scripts/sensor_bin_to_csv.py input.BIN output.csv
python scripts/csv_to_segmented_activity.py data.csv activities.xlsx Thigh
python scripts/segmented_activity_to_stack.py file1.npz file2.npz --window-size 250
python scripts/stack_to_features.py result.npz --output features.npz
```

### 6. Ventajas de la nueva nomenclatura

1. **Claridad**: Los nombres describen exactamente qué hace cada paso
2. **Consistencia**: Formato uniforme `input_to_output`
3. **Flujo lógico**: Refleja el pipeline de procesamiento de datos
4. **Autoexplicativo**: No requiere documentación adicional para entender el propósito

### 7. Pipeline completo de ejemplo

```bash
# Paso 1: Convertir datos binarios a CSV
sensor_bin_to_csv examples/data/PMP1020_W1_PI.BIN data_PI.csv

# Paso 2: Segmentar por actividades
csv_to_segmented_activity data_PI.csv activities.xlsx Thigh --output segmented_PI

# Paso 3: Crear stack para ML
segmented_activity_to_stack segmented_PI.npz --window-size 250 --output final_data.npz
```

## Estado final

✅ Todos los scripts renombrados y funcionando
✅ Comandos globales disponibles tras `pip install -e .`
✅ Documentación actualizada
✅ Nomenclatura consistente y descriptiva
✅ Pipeline completo de datos listo para usar

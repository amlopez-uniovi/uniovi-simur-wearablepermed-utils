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
sensor_bin_to_csv → csv_to_segmented_activity → segmented_activity_to_stack
```

1. **sensor_bin_to_csv**: Convierte datos de sensores desde formato binario (.BIN) a CSV
2. **csv_to_segmented_activity**: Segmenta datos CSV por actividades usando Excel de registro
3. **segmented_activity_to_stack**: Convierte datos segmentados a formato stack para ML

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
     sensor_bin_to_csv = uniovi_simur_wearablepermed_utils.bin2csv:run
     csv_to_segmented_activity = uniovi_simur_wearablepermed_utils.file_management:load_segment
     segmented_activity_to_stack = uniovi_simur_wearablepermed_utils.segmentation_cli:main
```

### 5. Uso después de la instalación

```bash
# Instalar en modo desarrollo
pip install -e .

# Usar comandos globalmente
sensor_bin_to_csv input.BIN output.csv
csv_to_segmented_activity data.csv activities.xlsx Thigh
segmented_activity_to_stack file1.npz file2.npz --window-size 250 --output result.npz

# O usar scripts directamente
python scripts/sensor_bin_to_csv.py input.BIN output.csv
python scripts/csv_to_segmented_activity.py data.csv activities.xlsx Thigh
python scripts/segmented_activity_to_stack.py file1.npz file2.npz --window-size 250
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

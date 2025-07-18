# Scripts de Línea de Comandos

Este directorio contiene scripts independientes para procesar datos WPM (Wearable Performance Monitoring) desde la línea de comandos.

## Pipeline de Procesamiento

Los scripts están diseñados para funcionar como un pipeline de procesamiento de datos:

1. **`sensor_bin_to_csv.py`** - Conversión de datos de sensor desde formato BIN a CSV
2. **`csv_to_segmented_activity.py`** - Segmentación de datos CSV por actividades
3. **`segmented_activity_to_stack.py`** - Conversión de datos segmentados a formato stack

## Scripts disponibles

### 1. `sensor_bin_to_csv.py` - Conversión BIN a CSV
Convierte archivos de datos de sensores desde formato binario (.BIN) a formato CSV legible.```bash
# Procesar datos de muslo y muñeca para PMP1020
segmented_activity_to_stack 
  examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_PI.npz 
  examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_M.npz 
  --crop-columns 1:7 
  --window-size 250 
  --step-size 125 
  --output data_PMP1020_combined.npz 
  --verbose
```

Esto producirá una salida similar a:
```
=== Segmented WPM Data Processing ===
Processing 2 files:
  1. examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_PI.npz
  2. examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_M.npz
Crop columns: slice(1, 7, None)
Window size: 250
Step size: 125

✓ Processing completed successfully!
✓ Stacked data shape: (1234, 12, 250)
✓ Number of labels: 1234
✓ Unique activities: 15

Label distribution:
  CAMINAR USUAL SPEED: 89 windows
  SENTADO VIENDO LA TV: 156 windows
  ...

✓ Results saved to: data_PMP1020_combined.npz
```

---

## Pipeline completo de procesamiento

Los scripts están diseñados para trabajar en secuencia:

```bash
# 1. Convertir archivos BIN a CSV
python sensor_bin_to_csv.py sensor_data.BIN sensor_data.csv

# 2. Convertir CSV a datos segmentados por actividad
python csv_to_segmented_activity.py sensor_data.csv activities.xlsx Thigh --output segmented_data

# 3. Convertir datos segmentados a formato stack
python segmented_activity_to_stack.py segmented_data.npz --window-size 250 --output final_data.npz
```

---

## Instalación y uso global

Después de instalar el paquete, los comandos estarán disponibles globalmente:

```bash
pip install -e .

# Usar comandos globalmente
sensor_bin_to_csv input.BIN output.csv
csv_to_segmented_activity data.csv activities.xlsx Thigh
segmented_activity_to_stack file1.npz file2.npz --window-size 250
```ivos .BIN de sensores a formato .CSV.

### 2. `csv_to_segmented_activity.py` - Conversión CSV a datos segmentados por actividad  
Carga, escala, segmenta y opcionalmente grafica datos WPM desde archivos CSV y Excel.

### 3. `segmented_activity_to_stack.py` - Conversión de datos segmentados a formato stack
Procesa datos WPM segmentados: carga, concatena, enventana y apila desde archivos NPZ.

---

## 1. BIN to CSV Conversion Script (`sensor_bin_to_csv.py`)

Este script convierte archivos .BIN de sensores al formato .CSV.

### Uso básico

```bash
python sensor_bin_to_csv.py input.BIN output.csv
```

### Ejemplos

#### 1. Conversión básica
```bash
python sensor_bin_to_csv.py sensor_data.BIN converted_data.csv
```

#### 2. Con rutas relativas y verbose
```bash
python sensor_bin_to_csv.py ../data/MATA00.BIN ../output/MATA00.csv --verbose
```

#### 3. Conversión de archivos de ejemplo
```bash
python sensor_bin_to_csv.py \
  ../examples/data/PMP1020_W1_PI.BIN \
  ../output/PMP1020_W1_PI_converted.csv \
  --verbose
```

### Parámetros

#### Obligatorios
- `bin_file`: Ruta al archivo .BIN de entrada
- `csv_file`: Ruta al archivo .CSV de salida

#### Opcionales
- `--verbose`, `-v`: Mostrar información detallada del proceso

### Formato de salida

El archivo CSV generado incluye las siguientes columnas:
- `dateTime`: Timestamp en milisegundos
- `acc_x`, `acc_y`, `acc_z`: Datos del acelerómetro (g)
- `gyr_x`, `gyr_y`, `gyr_z`: Datos del giroscopio (°/s)
- `bodySurface_temp`: Temperatura corporal (°C)
- `ambient_temp`: Temperatura ambiente (°C)
- `hr_raw`: Frecuencia cardíaca cruda
- `hr`: Frecuencia cardíaca procesada
- `remarks`: Comentarios del archivo

### Ejemplo de salida

```
Converting ../data/MATA00.BIN to ../output/MATA00.csv
✓ Conversion completed successfully!
```

---

## 2. CSV to Segmented Data Script (`csv_to_segmented_activity.py`)

Este script convierte datos CSV en datos segmentados WPM: carga, escala, segmenta y opcionalmente grafica.

### Uso básico

```bash
python csv_to_segmented_activity.py data.csv activities.xlsx Thigh
```

### Ejemplos

#### 1. Procesamiento básico con gráficos
```bash
python csv_to_segmented_activity.py data.csv activities.xlsx Thigh
```

#### 2. Procesar y guardar en archivo
```bash
python csv_to_segmented_activity.py data.csv activities.xlsx Thigh --output results
```

#### 3. Procesar sin gráficos y con muestra inicial personalizada
```bash
python csv_to_segmented_activity.py data.csv activities.xlsx Wrist --sample-init 1000 --no-plot
```

#### 4. Procesar datos WPM de ejemplo
```bash
python csv_to_segmented_activity.py \
  ../examples/data/PMP1020_W1_PI.CSV \
  ../examples/data/PMP1020_RegistroActividades.xlsx \
  Thigh --output PMP1020_processed --verbose
```

### Parámetros

#### Obligatorios
- `csv_file`: Ruta al archivo CSV con datos de MATRIX
- `excel_activity_log`: Ruta al archivo Excel con registro de actividades  
- `body_segment`: Segmento corporal donde está colocado el IMU (`Thigh`, `Wrist`, `Hip`)

#### Opcionales
- `--plot`: Mostrar gráficos de los datos segmentados (por defecto: True)
- `--no-plot`: No mostrar gráficos de los datos segmentados
- `--output`, `-o`: Nombre del archivo de salida (sin extensión) para guardar datos segmentados
- `--sample-init`: Índice de muestra para el inicio de "CAMINAR - USUAL SPEED"
- `--verbose`, `-v`: Mostrar información detallada del procesamiento

### Formato de entrada

- **CSV**: Debe contener datos de sensores MATRIX con columnas de tiempo y sensores
- **Excel**: Debe contener el registro de actividades con horarios de inicio y fin

### Ejemplo de salida

```
=== CSV to Segmented WPM Data Processing ===
CSV file: ../examples/data/PMP1020_W1_PI.CSV
Excel file: ../examples/data/PMP1020_RegistroActividades.xlsx
Body segment: Thigh
Show plots: True
Output file: PMP1020_processed
Sample init: Auto

Starting WPM data processing...
✓ Processing completed successfully!
```

---

## 3. Segmented Data to Stacked Data Script (`segmented_activity_to_stack.py`)

Este script procesa datos WPM segmentados desde archivos NPZ utilizando la función `load_concat_window_stack`.

## Instalación

Después de instalar el paquete, el comando `process_wmp_data` estará disponible globalmente:

```bash
pip install -e .
```

## Uso

### Sintaxis básica

```bash
segmented_activity_to_stack [archivos.npz] --window-size TAMAÑO [opciones]
```

### Ejemplos

#### 1. Procesamiento básico
```bash
segmented_activity_to_stack file1.npz file2.npz --crop-columns 1:7 --window-size 250
```

#### 2. Con paso de ventana y archivo de salida
```bash
segmented_activity_to_stack file1.npz file2.npz \
  --crop-columns 1:7 \
  --window-size 250 \
  --step-size 125 \
  --output result.npz
```

#### 3. Usando columnas específicas
```bash
segmented_activity_to_stack file1.npz file2.npz \
  --crop-columns 1,2,3,4,5,6 \
  --window-size 250
```

#### 4. Procesando datos WPM de ejemplo
```bash
segmented_activity_to_stack \
  examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_PI.npz \
  examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_M.npz \
  --crop-columns 1:7 \
  --window-size 250 \
  --output combined_data.npz \
  --verbose
```

## Parámetros

### Obligatorios
- `npz_files`: Rutas a los archivos NPZ a procesar (uno o más archivos)
- `--window-size`, `-w`: Tamaño de ventana en número de muestras

### Opcionales
- `--crop-columns`, `-c`: Columnas a seleccionar de los arrays
  - Formato slice: `"1:7"` (columnas 1 a 6)
  - Formato lista: `"1,2,3,4,5,6"` (columnas específicas)
  - Por defecto: `"1:7"`
- `--step-size`, `-s`: Tamaño del paso para el enventanado
  - Por defecto: igual al tamaño de ventana (sin solapamiento)
- `--output`, `-o`: Nombre del archivo de salida (formato .npz)
- `--verbose`, `-v`: Mostrar información detallada del procesamiento

## Formatos de entrada

Los archivos NPZ deben contener diccionarios con arrays de datos de actividades. Cada clave representa una actividad y cada valor es un array NumPy con los datos de sensores.

## Formato de salida

El script genera (opcionalmente) un archivo NPZ con:
- `concatenated_data`: Array apilado con todas las ventanas
- `labels`: Array con las etiquetas correspondientes a cada ventana

## Uso alternativo

### Como módulo de Python
```bash
python -m uniovi_simur_wearablepermed_utils.segmentation file1.npz file2.npz --crop-columns 1:7 --window-size 250
```

### Como script independiente
```bash
python scripts/segmented_activity_to_stack.py file1.npz file2.npz --crop-columns 1:7 --window-size 250
```

## Errores comunes

1. **"File not found"**: Verifica que las rutas a los archivos NPZ sean correctas
2. **"Invalid crop columns format"**: Usa formato `"start:end"` o `"col1,col2,col3"`
3. **"Window size must be positive"**: El tamaño de ventana debe ser mayor que 0
4. **"Step size must be positive"**: El tamaño del paso debe ser mayor que 0

## Ejemplo completo

```bash
# Procesar datos de muslo y muñeca para PMP1020
process_wpm_data \
  examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_PI.npz \
  examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_M.npz \
  --crop-columns 1:7 \
  --window-size 250 \
  --step-size 125 \
  --output data_PMP1020_combined.npz \
  --verbose
```

Esto producirá una salida similar a:
```
=== WPM Data Processing ===
Processing 2 files:
  1. examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_PI.npz
  2. examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_M.npz
Crop columns: slice(1, 7, None)
Window size: 250
Step size: 125

✓ Processing completed successfully!
✓ Stacked data shape: (1234, 12, 250)
✓ Number of labels: 1234
✓ Unique activities: 15

Label distribution:
  CAMINAR USUAL SPEED: 89 windows
  SENTADO VIENDO LA TV: 156 windows
  ...

✓ Results saved to: data_PMP1020_combined.npz
```

---

## 2. BIN to CSV Conversion Script (`sensor_bin_to_csv.py`)

Este script convierte archivos .BIN de sensores al formato .CSV.

### Uso básico

```bash
python sensor_bin_to_csv.py input.BIN output.csv
```

### Ejemplos

#### 1. Conversión básica
```bash
python sensor_bin_to_csv.py sensor_data.BIN converted_data.csv
```

#### 2. Con rutas relativas y verbose
```bash
python sensor_bin_to_csv.py ../data/MATA00.BIN ../output/MATA00.csv --verbose
```

#### 3. Conversión de archivos de ejemplo
```bash
python sensor_bin_to_csv.py \
  ../examples/data/PMP1020_W1_PI.BIN \
  ../output/PMP1020_W1_PI_converted.csv \
  --verbose
```

### Parámetros

#### Obligatorios
- `bin_file`: Ruta al archivo .BIN de entrada
- `csv_file`: Ruta al archivo .CSV de salida

#### Opcionales
- `--verbose`, `-v`: Mostrar información detallada del proceso

### Formato de salida

El archivo CSV generado incluye las siguientes columnas:
- `dateTime`: Timestamp en milisegundos
- `acc_x`, `acc_y`, `acc_z`: Datos del acelerómetro (g)
- `gyr_x`, `gyr_y`, `gyr_z`: Datos del giroscopio (°/s)
- `bodySurface_temp`: Temperatura corporal (°C)
- `ambient_temp`: Temperatura ambiente (°C)
- `hr_raw`: Frecuencia cardíaca cruda
- `hr`: Frecuencia cardíaca procesada
- `remarks`: Comentarios del archivo

### Ejemplo de salida

```
Converting ../data/MATA00.BIN to ../output/MATA00.csv
✓ Conversion completed successfully!
```

---

## 3. Load and Segment WPM Data Script (`load_segment_wpm_data.py`)

Este script carga, escala, segmenta y opcionalmente grafica datos WPM desde archivos CSV y Excel.

### Uso básico

```bash
python load_segment_wpm_data.py data.csv activities.xlsx Thigh
```

### Ejemplos

#### 1. Procesamiento básico con gráficos
```bash
python load_segment_wpm_data.py data.csv activities.xlsx Thigh
```

#### 2. Procesar y guardar en archivo
```bash
python load_segment_wpm_data.py data.csv activities.xlsx Thigh --output results
```

#### 3. Procesar sin gráficos y con muestra inicial personalizada
```bash
python load_segment_wpm_data.py data.csv activities.xlsx Wrist --sample-init 1000 --no-plot
```

#### 4. Procesar datos WPM de ejemplo
```bash
python load_segment_wpm_data.py \
  ../examples/data/PMP1020_W1_PI.CSV \
  ../examples/data/PMP1020_RegistroActividades.xlsx \
  Thigh --output PMP1020_processed --verbose
```

### Parámetros

#### Obligatorios
- `csv_file`: Ruta al archivo CSV con datos de MATRIX
- `excel_activity_log`: Ruta al archivo Excel con registro de actividades  
- `body_segment`: Segmento corporal donde está colocado el IMU (`Thigh`, `Wrist`, `Hip`)

#### Opcionales
- `--plot`: Mostrar gráficos de los datos segmentados (por defecto: True)
- `--no-plot`: No mostrar gráficos de los datos segmentados
- `--output`, `-o`: Nombre del archivo de salida (sin extensión) para guardar datos segmentados
- `--sample-init`: Índice de muestra para el inicio de "CAMINAR - USUAL SPEED"
- `--verbose`, `-v`: Mostrar información detallada del procesamiento

### Formato de entrada

- **CSV**: Debe contener datos de sensores MATRIX con columnas de tiempo y sensores
- **Excel**: Debe contener el registro de actividades con horarios de inicio y fin

### Ejemplo de salida

```
=== WPM Data Processing ===
CSV file: ../examples/data/PMP1020_W1_PI.CSV
Excel file: ../examples/data/PMP1020_RegistroActividades.xlsx
Body segment: Thigh
Show plots: True
Output file: PMP1020_processed
Sample init: Auto

Starting WPM data processing...
✓ Processing completed successfully!
```

---

## Instalación y uso global

Después de instalar el paquete, los comandos estarán disponibles globalmente:

```bash
pip install -e .

# Usar comandos globalmente
process_wpm_data file1.npz file2.npz --window-size 250
convert_bin_to_csv input.BIN output.csv
load_segment_wpm_data data.csv activities.xlsx Thigh
```

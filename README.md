# Proyecto_bank

Análisis exploratorio // Proyecto EDA realizado con Python, Pandas y Visual Studio Code.


1. Estructura del repositorio
─ README.md                  ← pasos seguidos + informe de resultados
├── requirements.txt
├── data/
│   ├── raw/                   ← datos originales sin modificar
│   │   ├── bank-additional.csv        (43.000 llamadas)
│   │   └── customer-details.xlsx      (3 hojas: 2012, 2013, 2014 · 43.170 clientes)
│   └── processed/
│       └── bank_marketing_clean.csv   ← datos limpios y unidos (43.000 filas × 34 columnas)
├── notebooks/
│   ├── 01_limpieza_y_union.ipynb      ← carga, limpieza, unión y nuevas variables
│   └── 02_analisis_y_graficos.ipynb   ← estadística descriptiva y gráficos
├── src/
│   └── funciones.py                   ← 3 funciones reutilizables
└── reports/
    ├── figures/                       ← 11 gráficos
    └── tables/                        ← tabla descriptiva



2. Pasos seguidos
2.1 Inspección inicial: problemas encontrados
Detalle de los problemas

Columnas sobrantes	`Unnamed: 0` (índice antiguo) y `latitude`/`longitude` (no aparecen en el enunciado)
Coma decimal	`cons.price.idx`, `cons.conf.idx`, `euribor3m` y `nr.employed` se leían como texto (`"93,994"`)
Fechas en español	`date` tiene formato `2-agosto-2019`; las columnas `contact_month` y `contact_year` del enunciado no existen en el archivo
Valores nulos	`age` 11,9 % · `default` 20,9 % · `euribor3m` 21,5 % · `education` 4,2 % · `housing` y `loan` 2,4 % · `cons.price.idx` 1,1 % · `job` 0,8 % · `date` 0,6 % · `marital` 0,2 %
`pdays = 999`	Significa "no contactado antes", no 999 días (41.412 filas)
`default` casi constante	Solo 3 clientes con valor 1
Valores imposibles	15 edades fuera del rango 18–90
Excel en 3 hojas	Hay que juntarlas; 170 clientes del Excel no aparecen en el banco

2.2 Decisiones de limpieza
Detalle de las decisiones tomadas

Columnas sobrantes	Eliminadas	No aportan información
Coma decimal	`str.replace(",", ".")` + `pd.to_numeric`	Para poder calcular con ellas
Fechas	Diccionario de meses → `pd.to_datetime`; se crean `contact_year` y `contact_month`	Formato español no estándar
Fechas nulas (248)	Se dejan nulas	Inventar una fecha falsearía los datos
Variable `y`	`yes`→1, `no`→0	Permite calcular la tasa de conversión con `mean()`
Nulos en `cons.price.idx` y `euribor3m`	Mediana de las filas con los mismos `emp.var.rate`, `cons.conf.idx` y `nr.employed`	Estos indicadores se repiten por periodo; la media global mezclaría épocas muy distintas. Probado: error 0 en `cons.price.idx` y 0,02 de media en `euribor3m`
Nulos en `job`, `marital`, `education`	Categoría `unknown`	No se pierde información ni se inventa
`pdays = 999`	Nueva columna `contactado_antes` y `pdays` pasa a nulo	999 no es un valor real
`age`	Imposibles → nulo; los nulos no se rellenan	Un 12 % de edades inventadas distorsionaría el análisis por edad; pandas ignora los nulos
Outliers (`duration`, `campaign`)	Se detectan con IQR (7,1 % y 5,8 %) pero no se eliminan	Son valores posibles e informativos

2.3 Unión de las tablas
Se apilaron las 3 hojas del Excel (guardando el año de la hoja en `anio_hoja`) y se unió por `id_` con un left join desde el banco. El 100 % de las 43.000 llamadas cruzó con un cliente (`indicator=True`). Los 170 clientes del Excel sin llamada se descartan.

2.4 Nuevas variables
`hijos_total` (niños + adolescentes), `grupo_edad` (`pd.cut`), `tramo_ingresos` (cuartiles con `pd.qcut`), `antiguedad_anios` (fecha de llamada − fecha de alta), `contactado_antes`.

2.5 Buenas prácticas
Diccionarios para mapear valores, bucles `for` y `zip` para no repetir código, funciones reutilizables en `src/funciones.py`, comentarios en cada paso y rutas relativas.

3. Informe de resultados
Tasa de conversión global: 11,27 % (4.844 suscripciones en 43.000 llamadas).
En `duration` y `campaign` la media está muy por encima de la mediana (258 s vs 179 s; 2,6 vs 2 contactos) porque hay llamadas muy largas y clientes muy insistidos; el cliente típico se describe mejor con la mediana.

3.1 Segmentos que más convierten
Segmento	Clientes	Conversión
Resultado de la campaña anterior = success	1.436	65,3 %
Edad 66+	566	45,9 %
Estudiantes	903	31,3 %
Euribor más bajo (0,63–1,29)	9.099	29,6 %
Jubilados	1.790	25,2 %
Contacto por móvil (vs. teléfono fijo 5,2 %)	27.396	14,7 %
Los que menos: blue-collar (6,9 %), services (8,1 %), entrepreneur (8,3 %) y clientes casados (10,2 %) frente a solteros (13,9 %).
Edad: el efecto tiene forma de U: convierten más los jóvenes (18–25: 20,8 %) y los mayores (56–65: 15,4 %; 66+: 45,9 %); los de 36–55 años son los que menos (≈ 8,6 %). Esto no se debe solo a que haya jubilados y estudiantes: sin ellos, los 66+ siguen en 48,1 % y los 18–25 en 15,4 %. (Análisis con los 37.865 clientes de edad conocida.)
Canal: llamar a móvil casi triplica la conversión del fijo.
Insistir tiene rendimientos decrecientes: 13,0 % con 1 contacto, 6,4 % con 6–10 y solo 3,0 % con más de 10.
Contacto previo: 8,8 % si no hubo campaña anterior frente a 21,1 % con 1 contacto previo y 47–75 % con 2 o más.

3.2 Contexto macroeconómico
`nr.employed` (r = −0,36), `euribor3m` (−0,31) y `emp.var.rate` (−0,30) son las variables macro más relacionadas con `y`. Con tipos bajos los clientes contratan más depósitos (29,6 % con euribor < 1,29 frente a 3,6–5,5 % con euribor > 4,15), algo coherente con que un depósito resulta más atractivo con tipos bajos. Estas tres variables están muy correlacionadas entre sí (r ≈ 0,91–0,97): miden casi lo mismo.

3.3 Duración de la llamada: ojo con la fuga de información
Es la variable más correlacionada con `y` (r = 0,40): quien suscribe habla una mediana de 449 s frente a 163 s. Pero la duración solo se conoce al terminar la llamada, así que no sirve para decidir a quién llamar; es una consecuencia del interés del cliente, no una causa.

3.4 Lo que NO influye
Variable	Conversión por grupos
Ingresos (cuartiles)	10,8 % – 11,5 %
Número de hijos	10,8 % – 11,7 %
Visitas web mensuales	11,2 % – 11,3 %
Mes de la llamada	10,3 % – 12,4 %, sin patrón
Año de la llamada	10,9 % – 11,7 %

3.5 Una relación engañosa
Los clientes de la hoja 2014 convierten al 23,0 % frente a 7,7 % (2013) y 4,6 % (2012). Parece que "los clientes más recientes responden mejor", pero al comparar solo clientes sin campaña previa y con euribor alto, las tres hojas quedan en 4,6 %, 5,6 % y 4,9 %: la diferencia desaparece. Las hojas siguen el orden temporal del dataset original y por eso se mezclan con el ciclo económico y el contacto previo. Es un ejemplo de que correlación no implica causalidad.

3.6 Recomendaciones
Priorizar clientes con campañas previas exitosas, jubilados, mayores de 65 y estudiantes.
Llamar a móvil siempre que se pueda.
Limitar los intentos a 3–4 por cliente.
Concentrar el esfuerzo comercial cuando los tipos de interés están bajos.
No segmentar por ingresos, hijos ni actividad web: no discriminan.

4. Limitaciones
Fechas incoherentes: las llamadas van de 2015 a 2019, pero los indicadores macro y `Dt_Customer` (2012–2014) corresponden a otro periodo, y las llamadas están repartidas casi uniformemente por mes y año. Parecen fechas asignadas de forma artificial, por lo que no se sacan conclusiones temporales.
Los indicadores macro toman pocos valores distintos (`nr.employed` solo 11), así que su efecto puede mezclarse con otros factores.
El análisis por edad excluye al 12 % de clientes sin edad.
Los resultados son asociaciones, no relaciones causales.

# Investigación: qué hace falta para lanzar a producción una app web con login

Fecha de lectura de las fuentes: 2026-11-17. Cada afirmación lleva su fuente entre corchetes, con el número de la lista final. Lo que no pude verificar en una fuente primaria se marca [secundaria]. El criterio propio sin fuente se marca [opinión]. Lo que no pude leer figura al final, en "Páginas que no pude leer".

Alcance: complementa a `investigacion.md` (contenido de la política de privacidad y de seguridad) y a `ejemplos.md`. No repite los artículos 12 a 14 del GDPR ni los artículos 4 a 16 de la ley 25.326 que ya están ahí; los cita solo cuando son parte de un procedimiento.

Aviso general: nada de esto reemplaza a un abogado. Donde dice "solo el dueño o un abogado" es porque la decisión depende de hechos del negocio (a quién se vende, desde qué entidad, dónde está el público) que el código no revela.

## Resumen de condiciones que la skill puede detectar

| Señal en el repo o respuesta del dueño | Dispara |
|---|---|
| Hay registro de usuarios o login | Términos y condiciones (sección 1), política de baja de cuenta, procedimientos de derechos (sección 5) |
| Se cobra (Stripe, Mercado Pago, `checkout`, `price_`, `subscription`) | Botón de arrepentimiento y de baja (secciones 1 y 7), PCI (sección 7), datos de la entidad cobradora |
| Cookies propias de sesión únicamente | Sin banner, pero tabla de cookies en la política (sección 2) |
| `gtag`, `fbq`, `ttq`, Hotjar, Meta pixel, SDKs publicitarios | Banner con consentimiento previo (sección 2), etiquetas de tienda con "seguimiento" (sección 6) |
| Proveedores fuera de Argentina (Vercel, Sentry, Prisma, GitHub, Google) | DPA, transferencia internacional (sección 4) |
| Usuarios en la UE o el Reino Unido | GDPR completo: registro de actividades, plazos, eventual DPO o evaluación de impacto (sección 5) |
| Bundle de iOS o Android | Etiquetas de privacidad, eliminación de cuenta dentro de la app, URL de política (sección 6) |
| Menores posibles (juegos, educación, edad no restringida) | Sección 7, edad mínima |
| Emails de marketing | Baja en cada envío (sección 7) |

---

## 1. Términos y condiciones

### Qué exige la norma (Argentina)

- Alcance. Consumidor es la persona física o jurídica que adquiere o utiliza bienes o servicios, "en forma gratuita u onerosa", como destinatario final [1, art. 1]. Una app gratuita para el público general entra en la ley. Una app solo para empresas que usan el servicio para producir queda fuera del consumo, pero igual rige el régimen de contratos por adhesión del Código Civil y Comercial [2, arts. 984 a 989] [opinión sobre el encuadre del caso concreto].
- Información. El proveedor debe dar información "cierta, clara y detallada" sobre las características esenciales y las condiciones de comercialización; es gratuita y, por defecto, en soporte físico salvo que el consumidor elija otro medio [1, art. 4]. El Código repite el deber y exige claridad [2, art. 1100].
- Contratos por adhesión. Las cláusulas generales deben ser "comprensibles y autosuficientes", de redacción "clara, completa y fácilmente legible". Las que reenvían a textos que no se facilitan antes o al celebrar el contrato "se tienen por no convenidas". La regla vale para la contratación electrónica [2, art. 985]. Las ambiguas se interpretan contra quien las redactó [2, art. 987].
- Cláusulas abusivas. Se tienen por no convenidas las que desnaturalizan las obligaciones o limitan la responsabilidad por daños, las que restringen derechos del consumidor o amplían los de la otra parte, y las que invierten la carga de la prueba [1, art. 37]. El Código suma las que no son "razonablemente previsibles" por contenido, redacción o presentación [2, art. 988] y la regla del desequilibrio significativo [2, art. 1119]. Un límite de responsabilidad "total" o una renuncia a daños es exactamente lo que cae.
- Jurisdicción. En contratos a distancia y electrónicos el lugar de cumplimiento es donde el consumidor recibió o debió recibir la prestación, ese lugar fija la jurisdicción y "la cláusula de prórroga de jurisdicción se tiene por no escrita" [2, art. 1109]. Para un consumidor argentino, una cláusula que obligue a litigar en Delaware o en otro país no se sostiene [opinión de aplicación al caso, sobre el texto citado].
- Publicar el contrato. Quien contrata con consumidores por adhesión debe publicar en su sitio web un ejemplar del modelo de contrato [1, art. 38]. La Resolución 271/2020 pidió que figure en la página de inicio, con un único hipervínculo, íntegro y sin remisiones a otros sitios, bajo el nombre "Contratos de adhesión - Ley N° 24.240 de Defensa del Consumidor", y que el usuario registrado pueda ver el contrato que firmó [5, arts. 1 a 5]. No verifiqué si hay normas posteriores que la modifiquen, salvo que la Disposición 954/2025 derogó dos resoluciones vecinas (316/2018 y 424/2020) y no menciona a la 271 [3, art. 10].
- Baja. Si el servicio se contrató por medio electrónico, el consumidor puede rescindir por el mismo medio, y la empresa debe enviar constancia en 72 horas [1, art. 10 ter]. Está prohibido cobrar preaviso, mes adelantado u otro concepto por la baja [1, art. 10 quáter]. La Disposición 954/2025 exige, a quienes comercializan a distancia por web o canales digitales, un link "botón de baja de servicio" a simple vista, en lugar destacado y en el primer acceso, sin registración previa ni otro trámite adicional; el proveedor debe informar un código de registro en 24 horas por el mismo medio y 60 días de adecuación [3, arts. 4, 5 y 8]. La Disposición 3/2026 aclara que se pueden pedir pasos razonables de verificación de identidad [4, art. 1].
- Atención al consumidor. Si hay atención por canal informático, el horario no puede ser menor a los días y horarios comerciales; si es solo telefónica o electrónica, mínimo 8 horas diarias hábiles; hay que publicar el canal y el área responsable [3, art. 6].
- Arrepentimiento: ver sección 7.

### Contenido mínimo habitual (no lo exige una norma en esa forma) [opinión]

Los puntos de la lista siguiente son práctica de mercado; lo único con respaldo normativo es lo de arriba. Para cada cláusula se indica el riesgo argentino ya identificado.

| Cláusula | Qué debe decir | Riesgo en Argentina |
|---|---|---|
| Identificación | Razón social o nombre, CUIT, domicilio, email y canal de reclamos | Falta de datos del proveedor [1, art. 4] [3, art. 6] |
| Objeto y aceptación | Qué es el servicio, que usar o registrarse implica aceptar, versión y fecha | Reenvío a texto no entregado antes se tiene por no convenido [2, art. 985] |
| Cuentas | Edad mínima, veracidad de datos, custodia de credenciales, una persona por cuenta | Ver sección 7 por menores |
| Uso aceptable | Lista de prohibiciones (abuso, scraping, contenido ilegal, ingeniería inversa) | Redacción clara y previsible [2, art. 988] |
| Contenido del usuario | El usuario conserva la titularidad y otorga una licencia limitada para operar el servicio | Una licencia amplia y perpetua es candidata a abusiva [opinión] |
| Licencia del software | Licencia limitada, revocable, no exclusiva sobre el servicio | Sin riesgo especial |
| Precios y pagos | Precio final, impuestos, renovación automática, cómo se baja | Cargos automáticos no solicitados [1, art. 35] y baja sin costo [1, art. 10 quáter] |
| Limitación de responsabilidad | Alcance razonable, sin excluir daños por dolo o culpa grave ni derechos del consumidor | Cláusula que limita responsabilidad por daños es nula [1, art. 37 a] |
| Suspensión y baja | Causas, preaviso, exportación de datos, qué se conserva | La baja del usuario debe ser sin trabas [1, art. 10 ter] |
| Cambios | Aviso previo por email o en la app, y derecho a rescindir si no acepta | Modificación unilateral sin aviso es candidata a abusiva [opinión] |
| Ley y jurisdicción | Ley argentina y tribunales del domicilio del consumidor | Prórroga de jurisdicción nula con consumidores [2, art. 1109] |
| Privacidad | Remisión a la política, ya entregada antes de aceptar | [2, art. 985] |
| Contacto y reclamos | Canal, horarios y área responsable | [3, art. 6] |

### Aceptación y prueba

- No encontré en fuente primaria una regla argentina que distinga clickwrap de browsewrap. Lo que dicen las normas leídas: el contrato por adhesión electrónico solo vincula con el texto entregado antes o al celebrarlo [2, art. 985]; el proveedor que usa medios electrónicos debe informar el contenido mínimo, la facultad de revocar y los riesgos del medio [2, art. 1107]; el oferente debe confirmar por vía electrónica y sin demora la aceptación [2, art. 1108]; la exigencia de forma escrita se cumple con soporte electrónico [2, art. 1106].
- Recomendación [opinión]: clickwrap (casilla sin tildar más botón "Crear cuenta", con links a términos y privacidad), nunca browsewrap (un pie de página que dice que usar el sitio implica aceptar). El riesgo del browsewrap es que no hay acto positivo ni constancia de que el usuario vio el texto.
- Qué guardar como prueba [opinión, alineado con la carga de demostrar el consentimiento en la privacidad: GDPR art. 7.1 [23] y el criterio 5 de la Resolución 4/2019 sobre acreditar quién prestó el consentimiento [15]]:
  - id de usuario, fecha y hora con zona, versión y hash del texto aceptado, URL de cada documento aceptado
  - IP o huella truncada, user agent
  - texto exacto de la casilla y del botón de esa versión
  - archivo versionado de cada versión publicada de los términos
  - email de confirmación (art. 1108 del Código [2])

### Qué hace la skill, el dueño y el abogado

- Skill: borrador con las cláusulas de arriba adaptadas a lo detectado, página `/terminos`, enlace desde el registro y el pie, tabla `terms_acceptances` y el texto de la casilla, aviso de cambios.
- Dueño: razón social, CUIT, domicilio, canal de reclamos, política de precios y renovación, qué datos se conservan tras la baja.
- Abogado: encuadre consumidor o no, validez de limitaciones de responsabilidad, ley aplicable cuando hay usuarios de varios países, revisión de cláusulas abusivas. DNU 70/2023 modificó el artículo 989 del Código según la nota de InfoLEG [2]; conviene que un abogado confirme qué otras normas cambiaron desde entonces.

---

## 2. Consentimiento y cookies

### Qué exige la norma

- ePrivacy, artículo 5.3 (UE). Guardar información o acceder a información ya guardada en el equipo del usuario (cookies, localStorage, píxeles, fingerprinting) requiere consentimiento salvo las excepciones de transmisión y de "estrictamente necesario". Las autoridades europeas coordinadas en la EDPB confirmaron que la colocación o lectura de cookies se rige por la ley nacional que transpone la directiva ePrivacy y que el tratamiento posterior se rige por el GDPR [18, ap. 1]. No pude leer el texto oficial de la directiva (EUR-Lex bloquea lecturas automáticas); lo anterior se apoya en el informe de la EDPB.
- Consentimiento válido. Por defecto no se puede colocar ninguna cookie que requiera consentimiento sin él, y se expresa con una acción positiva [18, ap. 7]. Las casillas premarcadas no valen [18, ap. 10]. La base jurídica para colocar o leer cookies no puede ser el interés legítimo [18, ap. 24]. Hay que poder demostrar el consentimiento [23, art. 7.1] y retirarlo es tan fácil como darlo [23, art. 7.3].
- Banner. Una gran mayoría de autoridades consideró que un banner sin opción de rechazar en ninguna capa donde hay botón de aceptar no cumple [18, ap. 8]. Un rechazo como simple enlace, escondido en un párrafo o fuera del marco del banner, sin apoyo visual, no produce consentimiento válido [18, ap. 14]. No hay un estándar único de colores o contraste, pero un botón de rechazo ilegible es engañoso [18, ap. 17 y 18]. El banner no debe dar la impresión de que hay que consentir para acceder, y una vía es permitir seguir navegando sin cookies desde el primer nivel [18, ap. 13].
- CNIL (Francia). Recomienda botones globales de aceptar y rechazar en el primer nivel, por ejemplo "tout accepter" y "tout refuser", y un acceso "personnaliser mes choix" en el mismo nivel [22, ap. 27 y 28]. Pide poder demostrar el consentimiento en cualquier momento, con mecanismos de prueba y registros con fecha, también por terceros que recogen consentimiento [22, ap. 46 a 48]. Los traceurs exentos no requieren consentimiento ni obligación de informar según la ley, pero recomienda informarlos en la política de privacidad y usar cada uno para una sola finalidad [22, ap. 49 a 51].
- Retiro. Hay que ofrecer una solución fácil de acceder una vez recogido el consentimiento, como un ícono flotante permanente o un enlace en un lugar visible y estandarizado; no se puede imponer una solución específica [18, ap. 32 y 35].
- ICO (Reino Unido, PECR). Es otra norma, pero útil como referencia: cinco excepciones (comunicación, estrictamente necesario, estadística, apariencia, emergencia). La de estadística y la de apariencia exigen "un medio simple de oponerse, gratuito". Finalizada el 29 de abril de 2026 [20] [21]. No aplica a la UE; no extrapolar la excepción estadística a la UE [opinión].
- Qué es "estrictamente necesario". El grupo de autoridades recordó el dictamen 04/2012 del WP29: las cookies que retienen preferencias del usuario sobre un servicio se consideran esenciales [18, ap. 30], y advirtió contra clasificar como esenciales cookies que no lo son [18, ap. 26]. La ICO da ejemplos de exentas: cookie de sesión tras iniciar sesión, carrito de compras, balanceo de carga, seguridad y detección de fraude, y aclara que si la misma tecnología se usa además para otro fin la excepción no aplica [21]. La CNIL cita como ejemplo un valor con el idioma preferido [22, ap. 49].
- Argentina. No encontré en fuentes primarias una norma específica de cookies. Lo aplicable es la ley 25.326: consentimiento libre, expreso e informado [7, art. 5, vía `investigacion.md`], deber de informar finalidad, destinatarios y responsable [8], y el criterio 5 de la Resolución 4/2019 (el responsable debe poder acreditar que quien consintió es el titular) [15]. Que no exista una regla específica no exime de informar [opinión].
- Novedad a vigilar: la EDPB y el SEPD emitieron el dictamen conjunto 2/2026 sobre la propuesta "Digital Omnibus", que toca online tracking [19]. No lo leí; podría cambiar el artículo 5.3.

### Cuándo aplica y cómo detectarlo [opinión de método]

Aplica cuando hay usuarios en la UE o el Reino Unido, o el dueño quiere un estándar único. Buscar en el repo:

| Qué | Dónde mirar |
|---|---|
| Cookies propias | `Set-Cookie`, `res.cookie(`, `cookies().set(`, `document.cookie`, opciones de librerías de sesión (`next-auth`, `lucia`, `iron-session`, `supabase`, `clerk`) |
| Almacenamiento local | `localStorage`, `sessionStorage`, `indexedDB`, service workers |
| Analítica | `gtag(`, `googletagmanager.com`, `plausible`, `posthog`, `umami`, `@vercel/analytics`, `matomo` |
| Publicidad y píxeles | `fbq(`, `connect.facebook.net`, `ttq`, `snap`, `linkedin insight`, imágenes 1x1, `hotjar`, `clarity` |
| Embebidos de terceros | iframes de YouTube, mapas, Intercom, Crisp, reCAPTCHA, fuentes remotas |
| Sentry | `Sentry.init`; revisar si usa Replay o recopila IP (ver su documentación) |

La skill debe verificar en la documentación oficial de cada proveedor si su SDK escribe cookies o almacenamiento, en lugar de asumirlo. No afirmo aquí qué escribe cada SDK porque no lo leí.

### Artefactos

1. Tabla de cookies y almacenamiento (en la política o en una página `/cookies`). Campos mínimos [opinión, alineados con lo que piden las fuentes de informar finalidad y destinatarios]:

| Nombre | Proveedor y país | Tipo (cookie, localStorage, píxel) | Finalidad | Categoría (necesaria, preferencias, analítica, marketing) | Duración | Primera o tercera parte | Requiere consentimiento (sí o no) y por qué |
|---|---|---|---|---|---|---|---|
| `session` | Propio | Cookie | Mantener la sesión iniciada | Necesaria | Sesión o 30 días | Primera | No: autenticación [21] |

2. Banner con: aceptar y rechazar al mismo nivel y con el mismo peso visual [18, ap. 8, 14, 18] [22, ap. 27]; botón "Configurar" para el detalle; sin casillas premarcadas [18, ap. 10]; nada de scripts no esenciales hasta aceptar [18, ap. 7]; control permanente para retirar [18, ap. 32].
3. Registro del consentimiento: id anónimo, fecha, versión del banner, elecciones por categoría, texto mostrado, país [22, ap. 46 a 48] [opinión sobre campos].
4. Carga condicional de scripts (gestor propio o `<script type="text/plain" data-category>`).

### Quién lo hace

- Skill: inventario por código, tabla, banner, bloqueo previo, registro.
- Dueño: confirmar que no hay otros tags cargados por GTM o por el panel de un proveedor; aceptar o no analítica; alcance geográfico.
- Abogado: solo si hay publicidad, perfilado, usuarios de la UE en volumen, o categorización dudosa de cookies.

---

## 3. Registro de bases de datos en Argentina

### Qué dice la norma

- Artículo 21: todo archivo, registro, base o banco de datos público, y privado destinado a proporcionar informes, debe inscribirse en el Registro habilitado por el órgano de control. El registro incluye como mínimo: nombre y domicilio del responsable, características y finalidad del archivo, naturaleza de los datos, forma de recolección y actualización, destino y personas a las que pueden transmitirse, modo de interrelacionar la información, medios de seguridad con la categoría de personas con acceso, tiempo de conservación, y forma y condiciones para ejercer acceso, rectificación y actualización [7, art. 21 inc. 1 y 2]. Ningún usuario de datos puede tener datos de naturaleza distinta a los declarados [7, art. 21 inc. 3].
- Artículo 24: los particulares que formen archivos, registros o bancos de datos "que no sean para un uso exclusivamente personal" deben registrarse conforme al artículo 21 [7, art. 24].
- La AAIP lo resume así: los archivos y bases públicos y privados "destinados a dar informes" deben estar inscriptos; los de uso exclusivamente personal están exceptuados; incumplir puede sancionarse [8]. Un considerando reciente de la Secretaría de Innovación recuerda que el Decreto 1558/2001 entiende por bases privadas destinadas a dar informes "aquellos que exceden el uso exclusivamente personal y los que tienen como finalidad la cesión o transferencia de datos personales", con o sin costo [17].
- Quién debe inscribirse. El responsable (persona humana o jurídica titular de la base). Los responsables extranjeros que tratan datos de personas argentinas sin estar establecidos en el país también deben inscribirse y la AAIP habilitó un formulario web específico en noviembre de 2022 [10].
- Trámite. La inscripción del responsable es requisito previo para registrar una base [9]. Por la Resolución 132/2018 los trámites de inscripción, modificación y baja se hacen por Trámites a Distancia (TAD) [11] [39 pagbam, secundaria: sin arancel, formulario simplificado, sin reinscripción anual]. La presentación es declaración jurada [39 jbb, secundaria]. Hay certificado de inscripción con QR y un isologo oficial [9] [39 pagbam, secundaria sobre el isologo]. No pude leer los pasos detallados del trámite en la página de la AAIP porque se cargan en acordeones que no aparecen en la lectura.
- Plazos: no encontré plazo legal de inscripción previo al lanzamiento; la ley exige la inscripción, no fija plazo en el texto del artículo 21 [7]. Cambios: hay que informar modificaciones y bajas en tiempo y forma; no hacerlo es infracción leve [39 pagbam, secundaria sobre la Resolución 240/2022].
- Sanciones. La ley prevé apercibimiento, suspensión, multa de $1.000 a $100.000, clausura o cancelación [7, art. 31]; las resoluciones 240/2022 y 244/2022 actualizaron la graduación, con topes mayores [39 pagbam, secundaria]. Tratar datos sin inscripción figura como infracción leve; no inscribir cuando la DNPDP lo requirió, grave [39 pagbam, secundaria].
- Estado del proyecto de reforma. La AAIP informó en diciembre de 2025 que el proyecto de 2023 (con notificación de incidentes en 72 horas, DPO y evaluación de impacto) perdió estado parlamentario en 2025 y que prepara otro [16]. Una nota de IAPP indica que el proyecto eliminaba el deber de registrar bases [secundaria, resultado de búsqueda, no leído] y otro resultado menciona un "proyecto 3397-D-2026" [secundaria, no leído; el PDF de Diputados no cargó]. Mientras no haya ley nueva rige el artículo 21.
- Criterio sobre excepciones. Hay una excepción expresa: uso exclusivamente personal [7, art. 24] [8]. Para una app con usuarios finales, el texto del artículo 24 y la lectura del Decreto 1558 [17] llevan a inscribir. Es la lectura prudente; el criterio de la AAIP sobre si una base de usuarios propia, sin informes ni cesión, está o no alcanzada no lo encontré escrito en una fuente primaria [opinión].

### Artefacto y reparto

- Skill: ficha lista para copiar al formulario, con los campos del artículo 21 completados desde el código: finalidad, categorías de datos (tabla de usuarios), forma de recolección (formularios, OAuth), destinatarios y transferencias (proveedores de la sección 4), seguridad (medidas y roles con acceso), conservación, y cómo ejercer derechos. Texto para el pie de la política con el número de inscripción cuando exista. Recordatorio de actualizar ante cada cambio.
- Dueño: trámite en TAD con CUIL o CUIT y clave fiscal, firma de la declaración jurada, conservar el certificado.
- Abogado: decidir si la base entra o no (criterio del dueño y riesgos), y casos de responsable extranjero.

---

## 4. Contratos con proveedores y transferencias internacionales

### GDPR artículo 28: contenido mínimo del acuerdo con un encargado

Es [secundaria, reproducción del texto oficial en gdpr-info.eu; EUR-Lex bloqueó la lectura] [23, art. 28]. El contrato debe ser escrito y fijar objeto, duración, naturaleza y finalidad, tipo de datos y categorías de titulares, y estipular que el encargado:

1. trata los datos solo con instrucciones documentadas del responsable, también en transferencias
2. exige confidencialidad a quienes acceden
3. aplica las medidas del artículo 32
4. respeta las condiciones para subencargados (autorización previa específica o general, con aviso de cambios y posibilidad de oponerse), y traslada las mismas obligaciones al subencargado
5. asiste al responsable en derechos de los titulares
6. asiste con los artículos 32 a 36 (seguridad, brechas, evaluación de impacto)
7. borra o devuelve los datos al terminar
8. permite auditorías y da la información necesaria

El contrato puede basarse en cláusulas tipo [23, art. 28.6].

### Transferencias a terceros países

- GDPR capítulo V. Sin decisión de adecuación, hace falta una garantía adecuada: cláusulas tipo de la Comisión, reglas corporativas vinculantes, códigos de conducta o certificaciones, y otras con autorización [23, art. 46].
- Data Privacy Framework (EE.UU.). La Comisión adoptó la decisión de adecuación el 10 de julio de 2023; el Tribunal General la confirmó y rechazó la anulación el 3 de septiembre de 2025 (caso T-553/23, Latombe) [24]. Hay apelación presentada el 31 de octubre de 2025 ante el Tribunal de Justicia (C-703/25) [40, resultado de búsqueda, no leí el expediente]. Consecuencia práctica: el DPF sigue vigente a la fecha, pero conviene que cada DPA incluya además cláusulas tipo como red de seguridad [opinión]. Vercel, Netlify, Sentry, GitHub y Prisma las incluyen (tabla abajo).
- Argentina. El artículo 12 prohíbe transferir a países sin nivel adecuado, salvo excepciones taxativas [7, art. 12]. La lista de países adecuados de la AAIP (Disposición 60/2016 y Resolución 34/2019) incluye UE y EEE, Reino Unido, Suiza, Guernsey, Jersey, Isla de Man, Islas Feroe, Canadá (solo sector privado), Andorra, Nueva Zelanda, Uruguay e Israel (solo datos con tratamiento automatizado) [12]. Estados Unidos no figura [12]. Para países no adecuados: excepciones del artículo 12, consentimiento expreso del titular, cláusulas contractuales modelo (Disposición 60/2016, dos modelos: cesión y prestación de servicios; y Resolución 198/2023, cláusulas de la Red Iberoamericana de Protección de Datos para responsable a responsable y responsable a encargado) o normas corporativas vinculantes (Resolución 159/2018) [12] [13]. Un contrato que difiera de los modelos se somete a la AAIP dentro de 30 días de la transferencia [8] [12]. Usar los modelos tal cual no requiere presentación [8].
- Qué significa para un proveedor de nube. La propia AAIP da como ejemplo el almacenamiento en la nube de una empresa estadounidense: los datos se transfieren a los servidores del proveedor y este es encargado [12]. Entonces: Vercel, Sentry, Prisma, GitHub, Google y similares son transferencias internacionales desde Argentina hacia un país no adecuado.
- No hay una fuente primaria que diga si el SCC de la UE que firma el proveedor satisface por sí solo a la AAIP. La Resolución 198/2023 afirma que las cláusulas modelo de la Red Iberoamericana son compatibles con las de la Disposición 60/2016 y recoge las cláusulas de la UE de 2021 como inspiración [13]. Si el DPA del proveedor no incluye el modelo argentino, conviene firmar el modelo de la Disposición 60/2016 (anexo II, prestación de servicios) o dejar constancia del consentimiento expreso [opinión; un abogado debe confirmarlo].
- Información al usuario. La política debe nombrar los países de destino y la garantía (sección 1.2 de `investigacion.md`).

### Dónde está el DPA de cada proveedor y cómo se acepta

| Proveedor | URL oficial del DPA | Cómo se acepta | Transferencias | Subprocesadores |
|---|---|---|---|---|
| Vercel | https://vercel.com/legal/dpa (actualizado el 17 de marzo de 2026) [25] | Forma parte de los términos Enterprise; para planes Enterprise y Pro el cliente es responsable y Vercel encargado; obliga al aceptar el acuerdo o al ejecutar el DPA [25]. El texto no nombra el plan gratuito; no asumir cobertura [opinión] | Anexo 3 con las cláusulas tipo 2021/914 y el addendum del Reino Unido [25] | Trust Center de Vercel en security.vercel.com según un resultado de búsqueda; no abrí la lista [secundaria] |
| Netlify | https://www.netlify.com/pdf/netlify-dpa.pdf [26] | "Incorporado por referencia" en los términos de Netlify; se puede descargar para el archivo [26] | Define las cláusulas tipo de la UE y el IDTA del Reino Unido [26] | https://www.netlify.com/legal/subprocessors, lista con fecha de incorporación y ubicación (por ejemplo AWS, Stripe) [26] |
| Sentry | https://sentry.io/legal/dpa (versión 5.1.0 del 29 de mayo de 2024) [27] | Opt-in electrónico: el DPA rige desde que se acepta; la página indica "Follow our instructions to enter into our DPA" y los pasos exactos no los pude ver [27] | Define las cláusulas tipo 2021/914 y el Data Privacy Framework [27]; hay documento aparte de transferencias | https://sentry.io/legal/subprocessors/ (versión 2.3.0 del 1 de junio de 2026), con RSS; aviso de 30 días y plazo para oponerse [27] |
| Prisma | https://www.prisma.io/legal/dpa (10 de septiembre de 2025) [28] | Rige mientras apliquen los términos del servicio; copia firmada: escribir a compliance@prisma.io y firman por e-signature [28] | Cláusulas tipo 2021, IDTA y marcos EE.UU.-UE, Reino Unido y Suiza (declara adhesión al DPF) [28] | Listados en https://trust.prisma.io; aviso por email y 28 días para objetar [28] |
| GitHub | https://github.com/customer-terms/github-data-protection-agreement [29] | Forma parte del GitHub Customer Agreement de la entidad cliente [29]. Existe versión para clientes no Enterprise (docs.github.com), que figura en una búsqueda y no pude abrir [secundaria] | Cláusulas tipo 2021/914, addendum del Reino Unido y cláusulas suizas [29] | https://docs.github.com/en/site-policy/privacy-policies/github-subprocessors, con aviso de nuevos al menos 30 días antes [29] |
| Google Cloud y Workspace | https://cloud.google.com/terms/data-processing-addendum [30] | "Incorporado" al acuerdo con Google; rige desde que el cliente lo aceptó [30] | No lo verifiqué en el texto | https://cloud.google.com/terms/subprocessors [30] |
| Google Analytics, Ads y otros donde Google es encargado | https://business.safety.google/processorterms/ [30] | Rige desde que el "Partner" hizo clic para aceptar o acordó los términos [30] | No lo verifiqué | Ver mismo sitio |
| Firebase | https://firebase.google.com/terms/data-processing-terms (modificado el 21 de agosto de 2024) [30] | Se acuerda con la contratación del servicio [30] | No lo verifiqué | No lo verifiqué |

### Artefactos y reparto

- Skill: inventario de proveedores a partir de dependencias y variables de entorno (por ejemplo `SENTRY_DSN`, `DATABASE_URL`, `VERCEL_`, `GOOGLE_`), tabla "proveedor, qué datos recibe, país, instrumento de transferencia, URL del DPA, URL de subprocesadores, fecha de revisión", y lista de pendientes de aceptar.
- Dueño: aceptar o firmar cada DPA desde la cuenta con facultades, guardar copia con fecha, suscribirse a avisos de subprocesadores, y firmar los modelos argentinos si se decide.
- Abogado: confirmar suficiencia del instrumento frente a la AAIP y analizar transferencias a países no adecuados con datos sensibles.

---

## 5. Procedimientos internos

### Incidentes o filtraciones

- GDPR. Notificar a la autoridad "sin demora indebida" y, de ser viable, dentro de 72 horas desde que se toma conocimiento, salvo que sea improbable que haya riesgo; si se pasa de 72 horas, con motivos del retraso. El encargado debe avisar al responsable sin demora. La notificación incluye naturaleza, categorías y cantidad aproximada de afectados y registros, contacto, consecuencias probables y medidas. Se puede dar por fases. Hay que documentar todas las brechas, incluso las no notificadas [23, art. 33]. Comunicar a los titulares sin demora cuando hay probable alto riesgo, en lenguaje claro; no hace falta si los datos estaban cifrados de forma ininteligible, si se tomaron medidas que eliminan el riesgo, o si sería un esfuerzo desproporcionado (entonces comunicación pública) [23, art. 34].
- Argentina. No encontré una norma en vigor que obligue al sector privado a notificar a la AAIP. La propia AAIP, al abrir una investigación en diciembre de 2025, dijo que no había recibido "notificación formal sobre un incidente... en los términos previstos por la normativa vigente" y que el proyecto que imponía 72 horas perdió estado parlamentario en 2025 [16]. Lo vigente es el deber de seguridad y confidencialidad del artículo 9 y 10 de la ley [7, arts. 9 y 10, vía `investigacion.md`] y la Resolución 47/2018, que derogó las disposiciones 11/2006 y 9/2008 y aprobó medidas de seguridad "recomendadas" para medios informatizados y no informatizados [14, arts. 1 a 3]. Sigue vigente según la AAIP, que la cita como medidas recomendadas para responsables [8]. Incluye un dominio de "Incidentes de seguridad": detección, evaluación, contención, respuesta, escalamiento y corrección [14, anexo I, dominio G]. Como atenuante, la graduación de sanciones considera la colaboración con la autoridad y las medidas correctivas ante incidentes [39 pagbam, secundaria sobre la Resolución 240/2022]. Práctica prudente [opinión]: notificar voluntariamente a la AAIP si el incidente afecta a personas en Argentina, y a la autoridad europea si hay usuarios de la UE.

### Pedidos de derechos

| Derecho | Argentina | GDPR |
|---|---|---|
| Acceso | 10 días corridos desde la intimación fehaciente; gratuito a intervalos no menores de seis meses salvo interés legítimo; sucesores universales en datos de fallecidos [7, art. 14] | Un mes, prorrogable dos meses más con aviso y motivos dentro del primer mes; gratis [investigacion.md, art. 12] |
| Rectificación, actualización o supresión | 5 días hábiles; si hubo cesión, notificar al cesionario dentro del quinto día hábil; no procede si perjudica derechos de terceros o hay obligación legal de conservar [7, art. 16] | Un mes igual que arriba; supresión por las causas del artículo 17 (fin del propósito, retiro del consentimiento, oposición, tratamiento ilícito, obligación legal, servicios a niños) con excepciones (libertad de expresión, obligación legal, defensa de reclamaciones, entre otras) [23, art. 17] |

Incumplir el plazo habilita la acción de hábeas data [7, arts. 14 y 16].

### Registro de actividades (art. 30), evaluación de impacto (art. 35), DPO (art. 37)

- Registro: obligatorio salvo para organizaciones de menos de 250 personas, y esa excepción cae si el tratamiento puede generar riesgo, no es ocasional, o incluye datos sensibles [23, art. 30.5]. Una app con login trata datos de forma no ocasional; por eso en la práctica el registro suele corresponder aunque seas una persona [opinión de aplicación]. Campos: responsable y contacto, finalidades, categorías de titulares y datos, destinatarios, transferencias con garantías, plazos de supresión, medidas de seguridad [23, art. 30.1].
- Evaluación de impacto: obligatoria antes del tratamiento cuando sea probable un alto riesgo; en especial evaluación sistemática y extensa de aspectos personales con decisiones de efectos significativos, tratamiento a gran escala de datos sensibles o penales, o monitoreo sistemático a gran escala de zonas públicas [23, art. 35.1 y 3]. Contenido mínimo: descripción de las operaciones, necesidad y proporcionalidad, riesgos, medidas [23, art. 35.7]. La autoridad publica listas de tratamientos que la requieren [23, art. 35.4].
- DPO: obligatorio para autoridades públicas, y cuando la actividad principal exige monitoreo regular y sistemático a gran escala, o tratamiento a gran escala de datos sensibles o penales [23, art. 37.1]. Puede ser externo; hay que publicar el contacto y comunicarlo a la autoridad [23, art. 37.6 y 37.7]. Un proyecto de una persona con login normal no suele cumplir [opinión]. En Argentina, la ley vigente no lo exige a privados; el proyecto de 2023 lo proponía [16].

### Esqueleto mínimo de runbook para un proyecto de una persona [opinión de método]

Archivo `runbook-datos.md` en el repo, con estas secciones.

1. Contactos. Quién decide (dueño), email de reclamos y de seguridad, abogado de guardia, autoridad (AAIP y la de la UE si aplica), contacto de cada proveedor.
2. Qué es un incidente. Acceso no autorizado, pérdida, filtración de claves, backup expuesto, error que muestra datos de otro usuario.
3. Primeras horas.
   - Anotar la hora en que te enteraste (arranca el reloj de 72 horas [23, art. 33.1]).
   - Contener: rotar claves y tokens, revocar sesiones, cortar el acceso, tomar copia de logs.
   - Evaluar: qué datos, cuántas personas, si estaban cifrados [23, art. 34.3].
4. Decisión de notificar. Árbol: ¿riesgo para las personas? ¿alto riesgo? ¿UE? Plantilla de aviso a la autoridad con los puntos del artículo 33.3 [23].
5. Aviso a usuarios. Plantilla en lenguaje claro: qué pasó, qué datos, qué hacer, contacto [23, art. 34.2].
6. Cierre. Causa raíz, correcciones, registro de la brecha (hechos, efectos, remedio) [23, art. 33.5].
7. Pedidos de derechos. Tabla con plazos (arriba), formulario o email, verificación de identidad, registro de cada pedido y respuesta, qué se conserva por obligación legal.
8. Revisiones. Registro de actividades, lista de proveedores y DPA, evaluación de impacto si cambia el riesgo [23, art. 35.11], medidas de la Resolución 47/2018 [14].

Quién: la skill genera el runbook y el registro de actividades desde el código; el dueño completa contactos y decide notificaciones; el abogado interviene ante una brecha real con riesgo alto.

---

## 6. Tiendas de apps

### App Store (Apple)

- URL de política obligatoria. Todas las apps deben incluir un enlace a su política en el campo de metadatos de App Store Connect y dentro de la app, en un lugar fácil de acceder [31, guía 5.1.1(i)]. La política debe identificar qué datos se recogen, cómo y todos los usos; confirmar que terceros (analítica, publicidad, SDKs) darán igual protección; y explicar la retención y eliminación y cómo revocar el consentimiento o pedir la eliminación [31, guía 5.1.1(i)]. En la ficha de producto, "Privacy Policy" es obligatorio y "Privacy Choices" es opcional [32].
- Etiquetas de privacidad (App Privacy Details). Hay que declarar en App Store Connect los datos que recoge la app y los de terceros cuyo código integrás, salvo los que cumplan todos los criterios de divulgación opcional; hay que mantener las respuestas actualizadas y se pueden cambiar sin enviar una versión [32]. "Recoger" es transmitir datos fuera del dispositivo de forma que el desarrollador o su socio puedan accederlos más tiempo del necesario para atender la solicitud [32]. Se declaran tipos de datos, usos, si están vinculados a la identidad y si se usan para seguimiento (tracking) [32]. Datos solo enviados y descartados tras atender el pedido no se declaran [32]. Apple también habla de firmas de SDKs de terceros y manifiestos de privacidad como parte de la cadena de suministro [32].
- Permiso y seguimiento. Las apps que recogen datos de uso deben obtener consentimiento aun siendo anónimos, con forma fácil de retirarlo [31, 5.1.1(ii)]; para seguimiento hay que pedir permiso con App Tracking Transparency [31, 5.1.2(i)]; compartir datos personales con IA de terceros exige divulgarlo y pedir permiso explícito [31, 5.1.2(i)].
- Eliminación de cuenta. Si la app permite crear cuenta, debe permitir iniciar su eliminación dentro de la app [31, 5.1.1(v)]. Detalle: ofrecer borrar el registro completo y los datos asociados (desactivar no alcanza), fácil de encontrar, enlace directo si hay que completar en la web, informar tiempos y qué se retiene; no exigir llamadas ni emails fuera de sectores muy regulados; se permite pedir reautenticación; con Sign in with Apple hay que revocar tokens por la REST API; las cuentas automáticas o de invitado también; borrar contenido generado por el usuario; si hay suscripciones, avisar que la facturación continúa en Apple; la eliminación debe estar disponible para todos y no solo donde lo exige la ley [33].
- Login. Si usás un login social de terceros como cuenta principal, tenés que ofrecer otro servicio equivalente que limite datos a nombre y email, permita ocultar el email y no rastree para publicidad sin consentimiento (por ejemplo Sign in with Apple), con excepciones [31, 4.8].

### Google Play

- Sección de seguridad de los datos (Data safety). Todos los desarrolladores deben completar el formulario en la página Contenido de la app de Play Console, incluso apps que no recogen datos, y dar un enlace a la política de privacidad; hay que agregar una política para completar el formulario y para que se muestre [34]. Se declara recolección, uso compartido, finalidades y prácticas de seguridad, incluyendo el código de SDKs de terceros; el desarrollador es responsable de que sea exacto y Google puede aplicar medidas (bloquear actualizaciones o retirar la app) [34]. Procesar datos de forma efímera (solo en memoria y solo el tiempo necesario) se incluye en la respuesta del formulario pero no se muestra en la ficha; los datos seudónimos sí deben declararse [34]. Cifrado en tránsito: seguir estándares como TLS o HTTPS [34].
- Eliminación de cuenta. Si la app permite crear una cuenta desde la app (o dirige a un flujo externo), debe ofrecer una ruta dentro de la app para eliminar la cuenta y sus datos, y un enlace web donde pedir la eliminación sin tener que reinstalar la app; ese enlace debe funcionar, mencionar el nombre de la app o del desarrollador y mostrar de forma destacada la vía de eliminación. Si se retiene algún dato por seguridad, fraude o ley, hay que informarlo, por ejemplo en la política. Aplica aunque algunas funciones se usen sin cuenta; las cuentas operadas sin conexión quedan fuera [35].
- Los plazos de cumplimiento de 2023 y 2024 que figuran en la guía ya vencieron; hoy basta con que el formulario y el enlace estén completos [35].

### Qué hace cada uno

- Skill: lista de datos recogidos por código y SDK con la traducción a las categorías de cada tienda, borrador de respuestas de las etiquetas y del formulario, página pública `/eliminar-cuenta` (con nombre de la app) y un endpoint o pantalla en la app para borrar la cuenta con revocación de tokens de login social, y la URL de política.
- Dueño: completar los formularios en App Store Connect y Play Console con su cuenta, declarar el estado de seguimiento, mantener las respuestas al día con cada release.
- Abogado: revisar declaraciones de seguimiento y sectores regulados.

---

## 7. Otros temas habituales

### 7.1 Edad mínima y menores

- Aplica si el servicio puede ser usado por menores o si el público incluye menores (educación, juegos, redes). Detectable por: campo de fecha de nacimiento, contenido dirigido a niños, preguntas del dueño.
- UE. Si la base es el consentimiento y se ofrecen servicios de la sociedad de la información directamente a un niño, el tratamiento es lícito desde los 16 años; por debajo hace falta autorización parental, con esfuerzos razonables de verificación, y los Estados pueden bajar el umbral hasta 13 [23, art. 8].
- EE.UU. COPPA aplica a servicios dirigidos a menores de 13 y a los de público general con conocimiento real de que recogen datos de menores de 13; no obliga a preguntar la edad, y quien filtra por edad de forma neutral puede confiar en lo declarado [36]. La regla enmendada rige desde el 23 de junio de 2025, con cumplimiento general hasta el 22 de abril de 2026 [36].
- Argentina. La Resolución 4/2019 (criterio 5) aplica la autonomía progresiva de los artículos 26 y 639 del Código: el menor puede consentir según su desarrollo; si no tiene capacidad suficiente, lo hace quien tiene la responsabilidad parental, con esfuerzos razonables de verificación [15]. No fija una edad numérica en el texto leído; hay una página de la AAIP que menciona tramos de 13 a 16 años y no la leí completa [secundaria].
- Artefacto: campo de edad o declaración, cláusula en términos ("tenés que tener 16 años o la autorización de tu madre, padre o tutor"), flujo de consentimiento parental si se aceptan menores. Dueño: decidir el público. Abogado: si se dirige a menores.

### 7.2 Pagos

- Aplica si la app cobra con tarjeta. Detectable por `stripe`, `mercadopago`, `payments`, formularios de tarjeta.
- PCI DSS es un estándar de la industria, no una ley. El esquema se declara con una autoevaluación (SAQ). Para comercios que tercerizan todo el procesamiento, la elegibilidad del SAQ A exige, según PCI DSS 4.0.1 desde el 1 de abril de 2025, confirmar que el sitio no es vulnerable a ataques por scripts: con técnicas como las de los requisitos 6.4.3 y 11.6.1 o con confirmación del proveedor de pago que embebe el formulario. Esa condición no aplica si se redirige a la página del proveedor [38].
- La forma más simple de reducir alcance [opinión]: usar la página de pago alojada o la redirección del proveedor, no tocar números de tarjeta en tu servidor ni logs.
- Artefacto: nota de alcance PCI en la documentación, y confirmar con el adquirente cuál SAQ corresponde [38]. Dueño: contrato con el procesador y la validación. Abogado: no hace falta salvo marketplace o pagos a terceros.

### 7.3 Email transaccional y marketing

- Aplica si la app envía emails. Detectable por Resend, SendGrid, Postmark, SES, SMTP.
- EE.UU. (CAN-SPAM): para emails comerciales, encabezados veraces, asunto no engañoso, identificar que es publicidad, dirección postal válida, opción de baja que se atienda en 10 días hábiles sin costo ni datos adicionales y que funcione al menos 30 días tras el envío. Los mensajes puramente transaccionales o de relación están exentos de la mayoría de las reglas, salvo encabezados veraces [37].
- Argentina. Quienes forman bancos de datos con fines de publicidad deben respetar que el titular pueda pedir en cualquier momento el retiro o bloqueo de su nombre [7, art. 27 inc. 3]; negarse es infracción grave [39 pagbam, secundaria]. El registro No Llame (ley 26.951) es para telefonía, no email [11].
- UE: el marketing por email requiere consentimiento previo según la directiva ePrivacy; no pude leer el texto y lo dejo como pendiente de verificación [opinión].
- Artefacto: enlace de baja en cada email de marketing, preferencias, separar flujos transaccionales y de marketing, registrar el origen del consentimiento, y dirección postal en el pie. Dueño: dirección legal. Abogado: campañas masivas o B2B en la UE.

### 7.4 Derecho de arrepentimiento si se cobra

- Aplica si se vende algo a distancia a consumidores. Detectable por checkout o suscripciones.
- El consumidor puede revocar en 10 días corridos desde la entrega o la celebración, lo último que ocurra; el derecho es irrenunciable, y hay que informarlo por escrito de forma clara y notoria en todo documento de venta [1, art. 34] [2, arts. 1110 y 1111]. Se notifica por escrito o por medios electrónicos, o devolviendo la cosa [2, art. 1112], y las partes se restituyen las prestaciones [2, art. 1113].
- Botón de arrepentimiento. Los proveedores que venden a distancia por web o similar deben tener, a simple vista, en lugar destacado y en el primer acceso, un link "botón de arrepentimiento" que permita revocar sin registración previa ni trámite adicional; el proveedor informa un código en 24 horas y debe efectivizar la revocación; 60 días de adecuación [3, arts. 1, 5 y 8]. Se pueden pedir pasos razonables solo para verificar identidad [4, art. 1]. Esto reemplaza a la Resolución 424/2020 [3, art. 10] [6].
- Excepciones: los casos del artículo 1116 del Código (productos personalizados o perecederos de rápido deterioro, grabaciones, programas informáticos descodificados y archivos descargables o reproducibles de uso inmediato y permanente, prensa) salvo pacto en contrario [2, art. 1116]; el servicio efectivamente usado o consumido; compras para reventa o integradas a un proceso productivo; productos perecederos [3, art. 3]. Eventos con fecha y turismo con fecha determinada tienen reglas especiales (aviso con 24 horas de antelación) [3, art. 2].
- Un SaaS por suscripción: el encuadre exacto (¿"servicio usado o consumido"?) lo debe decidir un abogado [opinión]; por defecto, ofrecer el botón y una política de reembolso clara, también por la baja del artículo 10 ter [1].
- Artefacto: botón en el pie del sitio y de la app web, formulario sin login que emite código, flujo de reembolso, texto del derecho en términos, factura y email de confirmación. Dueño: política de reembolsos. Abogado: encuadre de excepciones.

---

## Tabla final: qué documento o trámite, cuándo aplica, quién lo hace, dónde se publica o presenta

| Documento o trámite | Cuándo aplica | Quién lo hace | Dónde se publica o presenta |
|---|---|---|---|
| Términos y condiciones | Siempre que haya cuentas o servicio | Skill redacta, abogado revisa cláusulas de limitación y jurisdicción, dueño aporta datos legales | Página `/terminos`, enlace desde el registro, pie y la ficha de la tienda; modelo accesible desde la página de inicio [5] |
| Registro de aceptaciones | Siempre que haya cuentas | Skill (tabla y código) | Base de datos propia, no público |
| Botón de baja de servicio | Venta o contratación a distancia con cuenta o suscripción | Skill (UI y endpoint), dueño (proceso interno) | Primer acceso y lugar destacado del sitio [3] |
| Botón de arrepentimiento y política de reembolsos | Se cobra a consumidores | Skill (UI y flujo), dueño (política), abogado (excepciones) | Primer acceso del sitio y términos [3] |
| Datos de atención al consumidor | Atención por canal informático o telefónico | Dueño | Sitio web [3] |
| Política de privacidad y de seguridad | Siempre | Skill (ya cubierto en `investigacion.md`) | Sitio, tiendas, SECURITY.md |
| Política y tabla de cookies | Siempre se documenta; el banner solo si hay cookies o almacenamiento no esenciales | Skill, dueño decide qué herramientas de analítica o marketing se usan | `/cookies`, política de privacidad, banner en la app [18] [22] |
| Banner y registro de consentimiento | Hay analítica, publicidad, píxeles o embebidos de terceros no esenciales | Skill | App web [18] |
| Inscripción en el Registro Nacional de Bases de Datos | Base propia con datos de personas que no es de uso exclusivamente personal [7] [8] | Skill prepara la ficha, dueño presenta por TAD, abogado confirma alcance | Trámites a Distancia de la AAIP; número de inscripción en la política [9] [11] |
| DPA con cada proveedor | Hay proveedores que tratan datos de usuarios | Dueño acepta o firma, skill lista pendientes | Archivo interno; mención en la política [25] a [30] |
| Cláusulas de transferencia internacional (Disposición 60/2016 o Resolución 198/2023) | Proveedor en país no adecuado (EE.UU. entre ellos) y no hay otra vía | Abogado decide el instrumento, dueño firma | Archivo; solo se presenta a la AAIP si difiere de los modelos, en 30 días [8] [12] |
| Registro de actividades de tratamiento (art. 30) | Usuarios de la UE y tratamiento no ocasional [23] | Skill | Interno; disponible para la autoridad |
| Evaluación de impacto (art. 35) | Alto riesgo: perfilado con efectos significativos, datos sensibles a gran escala, monitoreo [23] | Dueño y abogado, skill ayuda con la plantilla | Interno |
| Designación de DPO (art. 37) | Monitoreo sistemático a gran escala o datos sensibles a gran escala [23] | Dueño | Contacto publicado y comunicado a la autoridad |
| Runbook de incidentes y de derechos | Siempre que se traten datos personales | Skill genera, dueño completa contactos | Repo (`runbook-datos.md`) |
| Etiquetas de privacidad de Apple | App en iOS [32] | Skill borrador, dueño completa | App Store Connect |
| Seguridad de los datos de Google Play | App en Android [34] | Skill borrador, dueño completa | Play Console |
| Eliminación de cuenta dentro de la app y página web | App con registro en tiendas [33] [35] | Skill | App, y enlace web en Play Console |
| Edad mínima y consentimiento parental | Menores posibles [15] [23] [36] | Skill (cláusula y campo), dueño (público), abogado (si va a menores) | Términos, registro |
| Alcance PCI DSS | Se cobra con tarjeta [38] | Dueño con el procesador | Interno, adquirente |
| Baja en emails de marketing | Hay emails de marketing [37] [7] | Skill | Cada email, preferencias |

---

## Fuentes

Primarias (texto de la norma, autoridades, documentación oficial):

1. Ley 24.240, texto actualizado, InfoLEG. https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/638/texact.htm
2. Código Civil y Comercial de la Nación (ley 26.994), texto actualizado, InfoLEG. https://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/235975/texact.htm
3. Disposición 954/2025, Subsecretaría de Defensa del Consumidor y Lealtad Comercial (botón de arrepentimiento y de baja). https://servicios.infoleg.gob.ar/infolegInternet/anexos/415000-419999/417152/norma.htm
4. Disposición 3/2026, Dirección Nacional de Defensa del Consumidor. https://www.boletinoficial.gob.ar/detalleAviso/primera/338248/20260206
5. Resolución 271/2020, Secretaría de Comercio Interior. https://servicios.infoleg.gob.ar/infolegInternet/anexos/340000-344999/341935/norma.htm
6. Resolución 424/2020, derogada por la 954/2025. https://servicios.infoleg.gob.ar/infolegInternet/anexos/340000-344999/342869/norma.htm
7. Ley 25.326, texto actualizado, InfoLEG. https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm
8. AAIP, Obligaciones de los responsables de bases de datos personales. https://argentina.gob.ar/aaip/datospersonales/responsables/obligaciones
9. AAIP, Trámites ante el Registro Nacional de Bases de Datos Personales (solo el encabezado cargó). https://argentina.gob.ar/aaip/datospersonales/tramites
10. AAIP, Registro para responsables extranjeros (2022). https://www.argentina.gob.ar/noticias/registro-de-bases-de-datos-personales-para-responsables-extranjeros
11. AAIP, nota sobre el Registro No Llame (menciona la Resolución 132/2018 y la inscripción). https://argentina.gob.ar/noticias/registro-no-llame-la-aaip-brinda-informacion-para-garantizar-el-cumplimiento-de-la-ley
12. AAIP, Transferencias internacionales. https://argentina.gob.ar/transferencias-internacionales
13. Resolución AAIP 198/2023 (cláusulas de la Red Iberoamericana). https://argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-198-2023-391538/texto
14. Resolución AAIP 47/2018 (medidas de seguridad recomendadas). https://servicios.infoleg.gob.ar/infolegInternet/anexos/310000-314999/312662/norma.htm
15. Resolución AAIP 4/2019, anexo (criterios orientadores). https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/318874/res4AAIP.pdf
16. AAIP, investigación de oficio por presunta filtración masiva (23 de diciembre de 2025). https://argentina.gob.ar/noticias/la-aaip-inicio-una-investigacion-de-oficio-ante-presunta-filtracion-masiva-de-datos
17. Resolución 296/2025 (Secretaría de Innovación), considerandos sobre el Decreto 1558/2001. https://servicios.infoleg.gob.ar/infolegInternet/anexos/420000-424999/420416/norma.htm
18. EDPB, Report of the work undertaken by the Cookie Banner Taskforce (17 de enero de 2023). https://www.edpb.europa.eu/system/files/2023-01/edpb_20230118_report_cookie_banner_taskforce_en.pdf
19. EDPB, página de Guidelines 05/2020 on consent (solo la ficha; el PDF no se leyó) y lista de documentos relacionados, con el dictamen conjunto 2/2026. https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en
20. ICO, Guidance on the use of storage and access technologies (actualizada el 29 de abril de 2026). https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/
21. ICO, What are the exceptions. https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/what-are-the-exceptions/
22. CNIL, Délibération 2020-092, recomendación sobre cookies y otros traceurs. https://cnil.fr/sites/cnil/files/atoms/files/recommandation-cookies-et-autres-traceurs.pdf
23. GDPR, artículos 3, 7, 8, 17, 28, 30, 33, 34, 35, 37 y 46. [secundaria: reproducción del texto oficial; EUR-Lex bloqueó la lectura] https://gdpr-info.eu/art-28-gdpr/ (y los mismos patrones para los demás artículos)
24. Tribunal de Justicia de la UE, comunicado sobre el caso T-553/23, Latombe v Commission. https://curia.europa.eu/site/upload/docs/application/pdf/2025-09/cp250106en.pdf
25. Vercel, Data Processing Addendum. https://vercel.com/legal/dpa
26. Netlify, DPA y GDPR/CCPA y subprocesadores. https://netlify.com/pdf/netlify-dpa.pdf , https://netlify.com/gdpr-ccpa , https://netlify.com/legal/subprocessors
27. Sentry, DPA y subprocesadores. https://sentry.io/legal/dpa , https://sentry.io/legal/subprocessors/
28. Prisma, Data Processing Agreement. https://prisma.io/legal/dpa
29. GitHub, Data Protection Agreement y subprocesadores. https://github.com/customer-terms/github-data-protection-agreement , https://docs.github.com/en/site-policy/privacy-policies/github-subprocessors
30. Google, Cloud Data Processing Addendum, DPA para productos donde Google es encargado, Firebase y subprocesadores. https://cloud.google.com/terms/data-processing-addendum , https://business.safety.google/processorterms/ , https://firebase.google.com/terms/data-processing-terms , https://cloud.google.com/terms/subprocessors
31. Apple, App Review Guidelines. https://developer.apple.com/app-store/review/guidelines/
32. Apple, App Privacy Details. https://developer.apple.com/app-store/app-privacy-details/
33. Apple, Offering account deletion in your app (guía 5.1.1(v)). https://developer.apple.com/support/offering-account-deletion-in-your-app/
34. Google Play Console Help, Provide information for Google Play's Data safety section. https://support.google.com/googleplay/android-developer/answer/10787469
35. Google Play Console Help, Understanding Google Play's app account deletion requirements. https://support.google.com/googleplay/android-developer/answer/13327111
36. FTC, COPPA FAQ y Federal Register, regla enmendada del 22 de abril de 2025. https://ftc.gov/tips-advice/business-center/guidance/complying-coppa-frequently-asked-questions , https://federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule
37. FTC, CAN-SPAM Act: A Compliance Guide for Business. https://ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
38. PCI Security Standards Council, FAQ sobre la elegibilidad del SAQ A (28 de febrero de 2025). https://blog.pcisecuritystandards.org/faq-clarifies-new-saq-a-eligibility-criteria-for-e-commerce-merchants

Secundarias (a confirmar):

39. Estudios jurídicos: PAGBAM sobre las resoluciones AAIP 132/2018, 240/2022 y 244/2022 (https://pagbam.com/articulos/continua-el-proceso-de-actualizacion-del-regimen-de-proteccion-de-datos-personales-nueva-clasificacion-y-graduacion-de-infracciones) y JBB sobre el registro (https://jbbabogados.com.ar/registro-de-bases-de-datos-personales-en-argentina-cuando-corresponde-inscribirlas-ante-la-aaip-y-como-hacerlo).
40. Resultado de búsqueda del expediente C-703/25 (apelación Latombe), https://curia.europa.eu/juris/liste.jsf?num=T-553/23 (no abierto).

## Páginas que no pude leer

- EUR-Lex (GDPR, directiva ePrivacy 2002/58/CE, decisión 2021/914 de cláusulas tipo, decisión del DPF): bloquea lecturas automáticas. Por eso el GDPR se cita desde gdpr-info.eu [secundaria] y el artículo 5.3 se apoya en el informe de la EDPB.
- EDPB, Guidelines 05/2020 (PDF) y Guidelines 2/2023 sobre el alcance técnico del artículo 5.3: el PDF no cargó (solo la ficha).
- Sitio de CNIL en inglés (404) y páginas de preguntas y respuestas de CNIL en francés: leí solo la recomendación 2020-092.
- Página de trámites de la AAIP para inscribir bases: solo el encabezado; los pasos están en acordeones que no aparecieron.
- Proyecto de ley 3397-D-2026 de Diputados (rest.hcdn.gob.ar): agotó el tiempo; dependo de la nota de la AAIP [16].
- GitHub DPA para clientes no Enterprise en docs.github.com (404 en la URL probada).
- Lista de subprocesadores de Vercel (Trust Center) y de Prisma (trust.prisma.io): no abiertas.
- Pasos exactos de aceptación del DPA de Sentry (la página remite a instrucciones que no vi).
- Cláusulas de transferencia en los DPA de Google y Firebase: no verifiqué su contenido.
- Texto de la Disposición 60/2016 y Resolución 34/2019: leí solo cómo las describe la AAIP.
- Página de la AAIP sobre capacidad de los menores (tramos de 13 a 16 años): solo un resultado de búsqueda.

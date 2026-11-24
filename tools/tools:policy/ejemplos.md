# Ejemplos reales: políticas de privacidad y de seguridad de cinco plataformas

Fecha de lectura: 2026-11-17. Todas las páginas se leyeron con TinyFish (fetch_content). Las citas son textuales y de 25 palabras o menos. Varios títulos originales están escritos en mayúsculas sostenidas en la fuente (PedidosYa, Lemon); acá se transcriben en sentence case y se avisa en cada caso.

Regla de lectura: lo que figura como "no se pudo leer" no se resume ni se infiere.

## 1. Mercado Libre (Argentina)

### Documentos

| Documento | URL exacta | Versión leída |
| --- | --- | --- |
| Declaración de privacidad y confidencialidad de la información | https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad | Sin fecha visible en la página. La versión 1.1 archivada en el mismo sitio muestra "Aug 11, 2021" en el buscador, pero no es la actual |
| Anexo para Argentina | https://mercadolibre.com.ar/privacidad/declaracion-privacidad/31199 | Sin fecha |
| Cuáles son tus derechos y cómo podés ejercerlos | https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad/31263 | Solo se leyeron los títulos; el detalle es desplegable y no se obtuvo |
| Con quién compartimos los datos | https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad/31274 | Sin fecha |
| Programa de recompensas en HackerOne | https://hackerone.com/mercadolibre | No se pudo leer (contenido dinámico). Solo se leyó el fragmento de búsqueda y el blog de HackerOne |

### Esqueleto de la declaración (títulos reales, en orden)

1. ¿Cómo aplica esta Declaración de Privacidad en Mercado Libre?
2. ¿Quién es el responsable del tratamiento de tus datos personales?
3. ¿Qué datos personales recolectamos y tratamos de vos? (subtítulos: ¿Cómo obtenemos tus datos?, ¿Qué tipo de datos recolectamos?)
4. ¿Para qué tratamos tus datos personales?
5. ¿Por qué recolectamos tus datos biométricos? (qué son, qué datos, cómo se protegen, derechos)
6. ¿A quién le compartimos tus datos personales? (subtítulos: ¿A quiénes compartimos tus datos?, ¿Cómo pueden usar otros usuarios tus datos?, ¿Cómo cuidamos tus datos cuando se transfieren a otro país?)
7. ¿Por cuánto tiempo guardamos tus datos personales?
8. ¿Cómo protegemos tus datos personales?
9. ¿Cuáles son tus derechos y cómo podés ejercerlos? (derechos, cómo ejercerlos, cómo oponerte, decisiones automatizadas, cookies)
10. ¿Qué ocurre si sos menor de edad y querés utilizar Mercado Libre?
11. ¿Qué ocurre si accedés a sitios o servicios de terceros desde Mercado Libre?
12. ¿Cuál es el Anexo aplicable a tu país?
13. Cambios en la Declaración de Privacidad
14. Glosario

Fuente del esqueleto: https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad

### Citas

- Consentimiento como condición: "prestar tu consentimiento voluntario, expreso e informado a esta Declaración de Privacidad es un requisito esencial para poder contratar" (https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad)
- Responsable, con CUIT y domicilio: "el responsable del tratamiento de tus datos es Mercado Libre SRL, CUIT 30-70308853-4, con domicilio en Avenida Caseros 3039" (https://mercadolibre.com.ar/privacidad/declaracion-privacidad/31199)
- Finalidades, con categorías: la página las agrupa en "Brindar los productos, servicios y/o beneficios", "Mejorar nuestros servicios", "Cumplir con obligaciones legales", "Detectar y prevenir fraudes", entre otras. Una finalidad llamativa: "Entrenar nuestros modelos de inteligencia artificial para poder brindarte una mejor experiencia dentro de nuestras plataformas" (https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad/para-que-tratamos-datos-personales_31076)
- Terceros, incluso proveedores de IA con nombre: "como OpenAI, Anthropic o Google, para habilitar, respaldar y/o mejorar ciertas funciones o servicios" (https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad/31274). Y la postura general: "Desde Mercado Libre no vendemos ni comercializamos datos que identifiquen a nuestros usuarios." (misma URL)
- Retención sin plazos numéricos: "Guardamos tus datos sólo durante el tiempo necesario para cumplir con los fines para los que los recopilamos." (https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad/duracion-guardado-datos-personales_31236)
- Derechos en el anexo argentino: "acceso, rectificación, supresión, oposición de tus datos personales" y remisión a la AAIP como órgano de control (https://mercadolibre.com.ar/privacidad/declaracion-privacidad/31199)
- Seguridad, con controles nombrados: "implementamos controles de acceso, políticas internas de seguridad de la información, procedimientos de gestión de incidentes y mecanismos de cifrado y monitoreo" (https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad/como-protegemos-tus-datos-personales_31248)

### Seguridad y divulgación

Programa público de recompensas en HackerOne, verificado en dos fuentes:

- Fragmento de la página del programa: "MercadoLibre offers rewards to eligible reporters for qualifying vulnerabilities, with a minimum reward of $50 USD." (https://hackerone.com/mercadolibre, leído solo en el resultado de búsqueda; la página no cargó)
- El director de Application Security de Mercado Libre cuenta que empezaron con programas privados en 2017 y lanzaron el público en 2023 (https://www.hackerone.com/blog/mercado-libres-journey-public-bug-bounty-program). Publica métricas: "16 hours to first response, one day to triage, on average, and three days as the average time to bounty." (misma URL)
- Hay además un programa de divulgación de vulnerabilidades separado, "MercadoLibre - Vulnerability Disclosure Program" (https://hackerone.com/mercadolibre_vdp/policy_versions), visto solo en un resultado de búsqueda.
- /.well-known/security.txt: respuesta 404 en www.mercadolibre.com.ar.

## 2. Didi (Argentina)

Nota de alcance: el dominio didi.org.ar es de otra organización (productos de credenciales digitales) y se descartó. Los documentos de DiDi Argentina viven en web.didiglobal.com y privacycenter.didiglobal.com.

### Documentos

| Documento | URL exacta | Versión leída |
| --- | --- | --- |
| Política global de procesamiento de datos personales (PDF bilingüe) | https://web.didiglobal.com/ar/legal/POL%C3%8DTICA-GLOBAL-DE-PROCESAMIENTO-DE-DATOS-PERSONALES_GLOBAL-PERSONAL-DATA-PROCESSING-POLICY.pdf | Fecha efectiva 29 de abril de 2024 |
| Términos y condiciones de uso del sitio (con un párrafo sobre uso de información personal) | https://web.didiglobal.com/ar/legal/terminos-y-condiciones/ | Sin fecha |
| Aviso de privacidad de DiDi Pasajero (Argentina) | https://privacycenter.didiglobal.com/AR/privacy-notice/f7ef99f4dd077eafbebf1daddb434b6a?id=395 | No se pudo leer: la página devolvió contenido vacío (se renderiza con JavaScript). Solo se conoce un fragmento de búsqueda |
| Centro de respuesta a incidentes de seguridad de DiDi (DSRC) | https://sec.didichuxing.com | Se leyó solo el menú (en chino): enviar vulnerabilidad, tienda de puntos, cuadro de honor, anuncios |

### Esqueleto de la política global (títulos reales, en orden; en el PDF alternan párrafos en español y en inglés)

1. Introducción
2. Definiciones
3. Información del responsable (remite al Anexo A)
4. Finalidades del tratamiento (4.1 Finalidades generales, 4.2 Proveedores y/o contratistas y su personal, y otras subsecciones)
5. Área responsable de atender consultas, solicitudes y reclamos de los titulares
6. Derechos del titular (6.1 a 6.8)
7. Procedimiento para el ejercicio de los derechos por parte del titular (consultas y reclamaciones)
8. Seguridad y confidencialidad de los datos personales
9. Vigencia de la base de datos
10. Fecha efectiva y modificaciones
Anexo A: entidades de DiDi que actúan como controladoras

### Citas

- Responsable por anexo: la política habla de "la entidad de DiDi que contrata los servicios de acuerdo con el" anexo A, sin nombrar una entidad argentina en el cuerpo (https://web.didiglobal.com/ar/legal/POL%C3%8DTICA-GLOBAL-DE-PROCESAMIENTO-DE-DATOS-PERSONALES_GLOBAL-PERSONAL-DATA-PROCESSING-POLICY.pdf)
- Canal y plazo de derechos: "serán atendidas en un plazo máximo de un mes a partir de la fecha de recepción de la solicitud" (misma URL, sección 7). El texto cita plazos de quince días hábiles para reclamos, que no coinciden con los de la Ley 25.326 (diez días corridos y cinco días hábiles). No se menciona la AAIP ni la Ley 25.326 en el texto leído.
- Derechos, con la lista de estilo GDPR: "El derecho a obtener del responsable del tratamiento información sobre los fines del procesamiento, las categorías de datos personales afectados, los destinatarios" (misma URL, 6.2)
- Retención, genérica: "Una vez que se cumpla el propósito del Tratamiento, los Datos Personales serán eliminados de los archivos de DiDi" (misma URL, sección 9)
- Seguridad: "DiDi has proactively integrated robust technical, organizational, and administrative measures across its operational processes." (misma URL, sección 8)
- Términos del sitio: "En DiDi hacemos un uso responsable de la información personal, protegiendo la privacidad de los Usuarios" (https://web.didiglobal.com/ar/legal/terminos-y-condiciones/)
- Fragmento del aviso de pasajeros (solo resultado de búsqueda, sin confirmar en la página): "DiDi no procesa ni procesará Datos Personales que correspondan a Usuarios o Pasajeros que sean menores de edad"

### Seguridad y divulgación

DiDi opera un centro de respuesta (DSRC) en https://sec.didichuxing.com, con login con cuenta DiDi, en chino, con recompensas (el fragmento de búsqueda habla de "奖励规范-V8.0" y bonificaciones de recompensa). No hay una política de divulgación específica para Argentina que se haya podido leer. No se encontró un security.txt ni un SECURITY.md propio de DiDi Argentina.

## 3. Uber

### Documentos

| Documento | URL exacta | Versión leída |
| --- | --- | --- |
| Aviso de privacidad para pasajeros y receptores de pedidos | https://www.uber.com/global/en/privacy-notice-riders-order-recipients/ (redirección desde https://privacy.uber.com/policy?lang=en-US) | "Last updated: October 22, 2026" |
| Aviso de privacidad para conductores y repartidores | https://uber.com/global/en/privacy-notice-drivers-delivery-people | No se leyó completo |
| Página de seguridad y bug bounty | https://www.uber.com/us/en/security/ | Sin fecha |
| Programa en HackerOne | https://hackerone.com/uber | No se pudo leer (contenido dinámico) |
| security.txt | https://www.uber.com/.well-known/security.txt | 404 |

Uber no tiene un aviso específico para Argentina; el aviso global incluye un apartado para cada país. Para Argentina solo agrega el dato de la AAIP.

### Esqueleto (títulos reales, en orden)

I. Overview (Scope)
II. Data collections and uses
- A. The data we collect
- B. How we use data
- C. Core automated processes
- (en el texto extraído la subsección D no aparece; sigue la E)
- E. Data sharing and disclosure
- F. Data retention and deletion
III. Choice and transparency (privacy settings, device permissions, in-app ratings pages, marketing and advertising choices)
IV. Legal information
- A. Data controllers and Data Protection Officer
- B. Our legal bases for using your data
- C. Legal framework for data transfers
- D. Updates to this Privacy Notice

### Citas

- Alcance claro y por perfil de usuario: "This notice applies when you use Uber’s apps or websites to request or receive products or services, including rides or deliveries." (https://www.uber.com/global/en/privacy-notice-riders-order-recipients/)
- Responsable: "Uber Technologies, Inc. is the sole controller of the data processed by Uber when you use Uber’s services globally" (misma URL, IV.A)
- Bases legales con tabla de usos por base: "Uber relies on the following legal bases for processing your data" y luego Contract, Consent, Legitimate interests, Legal obligation, cada una con su lista de usos (misma URL, IV.B)
- Terceros con nombres de intermediarios de publicidad: "Ad intermediaries, such as Criteo, Google, Rokt, The Trade Desk, TripleLift and others." (misma URL, II.E). También lista categorías de proveedores: almacenamiento en la nube, soporte, seguridad, IA y aprendizaje automático.
- Retención con plazos y tabla por categoría: "we delete such images within 48 hours unless longer retention is required by law" (misma URL, II.F). La tabla da "Account: Life of account" y otras categorías con "The sooner of life of account or 7 years".
- Canal para Argentina y autoridad: "The Agency of Access to Public Information, in its role of Regulating Body of Law 25.326, is responsible for receiving complaints" (misma URL, Overview)
- Borrado: "Users may request account deletion through the Uber apps and websites." (misma URL, II.F)

### Seguridad y divulgación

- "Uber uses the HackerOne platform to receive and review product-related vulnerabilities." y "our approach is to evaluate any given report based on the specific security impact for users" (https://www.uber.com/us/en/security/). Programa de bug bounty público verificado en la página de Uber; las reglas, el alcance y las recompensas viven en HackerOne y no se pudieron leer.
- security.txt: 404.

## 4. PedidosYa (Argentina)

### Documentos

| Documento | URL exacta | Versión leída |
| --- | --- | --- |
| Política de privacidad Argentina | https://www.pedidosya.com.ar/about/privacy_policies | Sin fecha visible en la página |
| Términos y condiciones generales | https://www.pedidosya.com.ar/terminos-y-condiciones | No se leyó |
| Reporte de vulnerabilidades del grupo Delivery Hero | https://www.deliveryhero.com/security/vulnerability-reporting/ | La página devolvió solo el pie de página; el texto del formulario se vio en un fragmento de búsqueda. No se confirmó que cubra a PedidosYa Argentina |
| security.txt | https://www.pedidosya.com.ar/.well-known/security.txt | 404 |

### Esqueleto (títulos reales, en orden; la fuente los escribe en mayúsculas)

1. Antecedentes preliminares
2. Principios que orientan la política (legalidad, libertad, finalidad, veracidad o calidad, transparencia, acceso y circulación restringida, seguridad, confidencialidad)
3. Responsable del tratamiento (con subsecciones sobre datos recolectados por categoría)
4. Actualización de la información
5. Con quién compartimos sus datos personales
6. A qué países transferimos sus datos
7. Sus derechos
8. Información sobre cookies
9. Seguridad de su información personal y servidores
10. Cambios en esta declaración de privacidad
11. Nota sobre el uso de este sitio por parte de niños
12. Disposiciones finales
13. Jurisdicción y ley aplicable
14. Consentimiento

### Citas

- Responsable: "el responsable de la base de datos es" PedidosYa S.A., CUIT 30-71198576-6 (la fuente escribe la razón social en mayúsculas) (https://www.pedidosya.com.ar/about/privacy_policies). Nota: el domicilio de la sección es distinto del que figura en el pie de la página de ayuda, que también lo da.
- Base: consentimiento. "El tratamiento de datos personales, sólo se llevará a cabo con el consentimiento, previo, expreso e informado del usuario." (misma URL, principio de libertad). No nombra otras bases legales.
- Terceros, por categorías y sin nombres: la lista incluye "Procesadores y facilitadores de pagos", "Proveedores de almacenamiento en la nube", "Proveedores de análisis de datos". Sí nombra a Google Analytics: "Utilizamos Google Analytics para analizar el uso de este sitio web." (misma URL, cookies)
- Transferencias: "algunos de nuestros proveedores de servicios tienen su sede en Estados Unidos" y procesamiento "principalmente dentro de Argentina, Uruguay y dentro de la Unión Europea" (misma URL)
- Retención: "PedidosYa retiene la información del usuario y el perfil por el tiempo en que usted mantenga su cuenta en PedidosYa." (misma URL). Aclara qué queda tras borrar: solo registros de pedidos "sin ser asociados a ninguna cuenta", para prevención de fraude y estadística.
- Derechos con plazos de la ley argentina: "podrá ejercer tales derechos dentro de los 5 (cinco) días hábiles de acreditada su identidad" y diez días corridos para el acceso. Canal: "por favor escribanos un email a datospersonales@pedidosya.com" y autoservicio en "Mi Cuenta" y "Ayuda en línea". Menciona a la AAIP como órgano de control.
- Seguridad realista: "ninguna medida de seguridad de datos puede garantizar por completo la protección en todo momento" (misma URL)

### Seguridad y divulgación

No hay una política de divulgación propia de PedidosYa Argentina que se haya podido leer. El grupo Delivery Hero tiene una página de "Vulnerability Reporting" (https://www.deliveryhero.com/security/vulnerability-reporting/) cuyo fragmento de búsqueda dice: "If you have discovered security vulnerabilities or would like to report any other security incident, please send us a" (cortado). No se pudo verificar alcance, plazos ni puerto seguro, ni si se aplica a PedidosYa.

## 5. Lemon (Lemon Cash, Argentina)

### Documentos

| Documento | URL exacta | Versión leída |
| --- | --- | --- |
| Declaración de privacidad Argentina | https://lemon.me/arg-terms/declaraci%C3%B3n-de-privacidad (redirige a https://lemon.me/en/argentina-terms/declaraci%C3%B3n-de-privacidad, que se sirvió en inglés) | "Last updated: 11/16/2023" (en la fuente va en mayúsculas) |
| Políticas de cookies | https://lemon.me/en/argentina-terms/pol%C3%ADticas-de-cookies | No se leyó (una URL anterior, /en/legales/cookies, devolvió 404) |
| security.txt | https://lemon.me/.well-known/security.txt | Leído, sin fecha |

### Esqueleto (títulos reales, en orden; la fuente los escribe en mayúsculas)

1. About this privacy statement
2. Data controller
3. What types of personal data do we process (data provided during registration, during platform use, obtained from data analysis, obtained from public or external access sources)
4. What do we use your personal data for (possible legal bases, possible purposes)
5. What are cookies and what do we do with them
6. With whom we share your personal data
7. How we make international transfers of personal data
8. What are your rights as a data subject
9. About operations carried out on blockchain
10. How long we store your personal data

### Citas

- Responsable: la política de Argentina dice que "The Place is a company incorporated in the Republic of El Salvador", mientras que el pie de la página nombra a Bay Treasure Caramel S.A. (CUIT 30-71753495-2) como proveedor de activos virtuales registrado en la CNV (https://lemon.me/en/argentina-terms/declaraci%C3%B3n-de-privacidad). El texto leído no menciona la Ley 25.326 ni la AAIP.
- Bases legales nombradas (consentimiento, ejecución del contrato, obligación legal e interés legítimo): "We will use your personal data if they are necessary for the satisfaction of legitimate interests pursued by The Place or by a third party" (misma URL)
- Terceros por categoría, sin nombres: la política lista grupo corporativo, proveedores, aliados comerciales, usuarios vinculados y autoridades. "The Place does not market or will market your personal data in any way." (misma URL)
- Transferencias: "we will implement additional technical and/or organizational security measures to guarantee the protection of your personal data" y cita cláusulas modelo y normas corporativas vinculantes (misma URL)
- Derechos: acceso, rectificación, supresión y oposición, ejercibles escribiendo al correo del DPO (dpo@lemon.me en el texto, escrito en mayúsculas en la fuente). Sin plazo propio: "within the period established by current law".
- Retención sin plazos: "The Place will keep your personal data as long as they are necessary to achieve the purposes for which they were collected" (misma URL). Sección propia sobre blockchain, donde los datos no se pueden borrar.
- Datos recogidos con detalle: dirección IP, ID de dispositivo, historial de navegación y geolocalización si el usuario la autorizó (misma URL, "Browsing data on our platform" y "Location data")

### Seguridad y divulgación

security.txt leído directamente (https://lemon.me/.well-known/security.txt):

- "we're going to answer all communications quickly and with respect and absolute confidentiality." 
- Contacto: un correo de ciberseguridad con el asunto exclusivo "BugBounty".
- El archivo no tiene el campo Expires, que el RFC 9116 exige [ver investigacion.md, sección 2.2]. No tiene Policy, ni puerto seguro.
- [secundaria] El directorio disclose.io lista un contacto de ciberseguridad de lemon.me, con "Safe Harbor: None" y fecha 23 de marzo de 2026 (https://directory.disclose.io/lemon-124d2a). Otro sitio de terceros afirma que hay un programa en HackerOne; no se verificó en una fuente de la empresa.

## 6. Tabla comparativa

Criterio: "sí" solo si se leyó en el documento. "Parcial" cuando es por categoría o genérico.

| Plataforma | Lista subprocesadores | Da plazos de conservación | Nombra bases legales | Canal de derechos | Divulgación de vulnerabilidades |
| --- | --- | --- | --- | --- | --- |
| Mercado Libre | Parcial: por categoría, con proveedores de IA nombrados (OpenAI, Anthropic, Google); remite a una lista de principales destinatarios que no se leyó | No: "el tiempo necesario", sin cifras | No de forma explícita en las páginas leídas; el consentimiento es central | Sí, Centro de privacidad, con AAIP como autoridad; detalle del procedimiento no leído | Sí: bug bounty público y VDP en HackerOne; sin security.txt |
| Didi | No (el PDF no lista terceros por nombre; el aviso de pasajeros no se leyó) | No, solo "una vez cumplido el propósito" | No de forma explícita; hace referencia a autorización y consentimiento | Sí, área legal y plazo de un mes, pero sin referencia a AAIP ni a los plazos argentinos | Parcial: centro de respuesta (DSRC) global, en chino, con login; nada específico para Argentina |
| Uber | Parcial: categorías, con intermediarios de publicidad nombrados | Sí: tabla por categoría, 7 años, 48 horas para imágenes de documento | Sí: tabla de bases con los usos de cada una | Sí: Privacy Center en la app, formulario y DPO; menciona a la AAIP para Argentina | Sí: bug bounty en HackerOne enlazado desde la página de seguridad |
| PedidosYa | Parcial: categorías; solo Google Analytics con nombre | Parcial: "mientras mantenga su cuenta", más qué queda tras el borrado | No: consentimiento como principio, sin tabla de bases | Sí: correo de datos personales, autoservicio en la app, plazos de la Ley 25.326 y AAIP | No encontrado para Argentina; el grupo tiene página de reporte (no verificada) |
| Lemon | Parcial: categorías sin nombres | No: "el tiempo necesario" | Sí: consentimiento, contrato, obligación legal e interés legítimo | Sí: correo del DPO; sin plazo propio ni mención de la AAIP | Parcial: security.txt con contacto y asunto, sin Expires ni puerto seguro |

## 7. Patrones que se repiten

A imitar:

1. Tabla de bases legales con los usos de cada base (Uber). Convierte la lista abstracta del GDPR en algo que se puede auditar contra el código. La skill puede generar esa tabla desde las finalidades detectadas.
2. Tabla de retención por categoría de dato (Uber). Es el único de los cinco que da cifras. La skill debe leerlas de los jobs de borrado, TTL y migraciones, y preguntar lo que falte.
3. Aclarar qué sobrevive al borrado (PedidosYa: registros de pedidos sin cuenta para fraude y estadística; Uber: 7 años por obligaciones fiscales). Evita una promesa de "borramos todo" que el código no cumple.
4. Un canal concreto de derechos con plazos locales y mención a la autoridad (PedidosYa con los 10 días corridos y 5 días hábiles de la Ley 25.326 y la AAIP; Uber y Mercado Libre nombran a la AAIP). Es lo que la AAIP pide que esté en la política [investigacion.md, sección 1.2].
5. Nombrar a los terceros con impacto, no solo categorías (Mercado Libre nombra proveedores de IA; Uber nombra intermediarios de publicidad; PedidosYa nombra Google Analytics). La skill puede nombrar los que detecta en las dependencias y el código.
6. Una frase de honestidad sobre los límites de la seguridad (PedidosYa: ninguna medida garantiza protección total; Mercado Libre excluye acciones ilícitas de terceros fuera de su control). Es coherente con lo que sugiere OWASP.
7. Una página separada de reporte de vulnerabilidades, enlazada desde seguridad (Uber), y un contacto que se pueda encontrar sin cuenta. Agregar security.txt con Contact y Expires, que ninguno de los cinco cumple completo.

A evitar:

8. Texto global y genérico aplicado a Argentina sin adaptación (Didi: plazos de reclamo que no son los de la ley argentina y sin mención de la AAIP; Lemon: responsable salvadoreño y ninguna mención de la Ley 25.326 en el texto leído). La skill debe preguntar la jurisdicción y no mezclar regímenes.
9. Retención como "el tiempo necesario" sin criterio (Mercado Libre, Lemon, Didi). Cumple de forma mínima la letra del GDPR si se dan criterios, pero no informa. Si el código tiene un TTL, ponerlo.
10. Mayúsculas sostenidas en títulos y listas (PedidosYa, Lemon) y consentimiento omnibus como condición de uso (Mercado Libre, PedidosYa). La skill debería evitar ambos.
11. security.txt incompleto: el de Lemon no tiene Expires y exige un asunto exclusivo; el RFC pide Expires y que el contacto sea una URI utilizable.

## Páginas que no se pudieron leer

- https://hackerone.com/mercadolibre, https://hackerone.com/mercadolibre_vdp/policy_versions y https://hackerone.com/uber (vacías, contenido dinámico)
- https://privacycenter.didiglobal.com/AR/privacy-notice/f7ef99f4dd077eafbebf1daddb434b6a?id=395 (aviso de DiDi Pasajero, vacío)
- Detalle desplegable de varias secciones de Mercado Libre (qué datos recolecta, derechos, lista de principales destinatarios)
- https://www.deliveryhero.com/security/vulnerability-reporting/ (solo pie de página)
- https://sec.didichuxing.com (solo menú, en chino, con login)
- https://lemon.me/en/argentina-terms/pol%C3%ADticas-de-cookies y las políticas de cookies de las otras plataformas (no se intentó el resto)
- https://www.pedidosya.com.ar/terminos-y-condiciones y https://uber.com/global/en/privacy-notice-drivers-delivery-people (no leídos)
- security.txt: 404 en mercadolibre.com.ar, uber.com y pedidosya.com.ar

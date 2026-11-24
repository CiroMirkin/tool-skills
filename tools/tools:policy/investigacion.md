# Investigación: qué deben contener una política de privacidad y una política de seguridad

Fecha de lectura de las fuentes: 2026-11-17. Cada afirmación lleva su fuente entre corchetes, con el número que corresponde a la lista del final. Lo que solo aparece en fuentes secundarias se marca [secundaria]. Lo que es criterio propio sin fuente se marca [opinión].

Alcance: sirve para que una skill genere (a) la política de privacidad de una app web, (b) la política de seguridad publicada como página de la app y (c) un SECURITY.md, a partir de leer el código real.

## 1. Política de privacidad

### 1.1 GDPR, artículos 12 a 14 (información obligatoria)

El artículo 12 fija cómo se informa: de forma concisa, transparente, inteligible y de fácil acceso, con lenguaje claro y sencillo, y con especial cuidado si va dirigida a un niño [1, art. 12.1]. La información es gratuita [1, art. 12.5]. El responsable responde las solicitudes de derechos en un mes, prorrogable dos meses más con aviso y motivos en el primer mes [1, art. 12.3]. Si no da curso a la solicitud, informa en el mismo plazo de un mes las razones, la posibilidad de reclamar ante la autoridad de control y de ir a la justicia [1, art. 12.4].

Cuando los datos se obtienen de la persona (artículo 13), al momento de obtenerlos hay que dar [1, art. 13.1 y 13.2]:

1. Identidad y datos de contacto del responsable y, si corresponde, de su representante.
2. Datos de contacto del delegado de protección de datos, si existe.
3. Fines del tratamiento y base jurídica.
4. Intereses legítimos, cuando esa sea la base.
5. Destinatarios o categorías de destinatarios.
6. Intención de transferir a un tercer país, si existe o no decisión de adecuación, y referencia a las garantías y cómo obtener copia.
7. Plazo de conservación o, si no se puede, los criterios para fijarlo.
8. Derechos de acceso, rectificación, supresión, limitación, oposición y portabilidad.
9. Derecho a retirar el consentimiento en cualquier momento, cuando la base es el consentimiento.
10. Derecho a reclamar ante una autoridad de control.
11. Si dar los datos es un requisito legal o contractual, o necesario para contratar, y qué pasa si no se dan.
12. Existencia de decisiones automatizadas, incluida la elaboración de perfiles, con información significativa sobre la lógica aplicada.

Si se quiere usar los datos para otro fin distinto del original, hay que informar antes de ese tratamiento [1, art. 13.3].

Cuando los datos no vienen de la persona (artículo 14, por ejemplo datos que llegan de un login con Google, de un proveedor de verificación o de una API de terceros) se informa lo mismo, más las categorías de datos y la fuente de la que proceden, incluso si es de acceso público [1, art. 14.1 y 14.2]. El plazo para informar es razonable y a más tardar un mes, o en la primera comunicación si los datos sirven para contactar a la persona [1, art. 14.3].

Otros artículos del mismo reglamento que condicionan el contenido: los principios de limitación de la finalidad y del plazo de conservación [1, art. 5], las bases de licitud [1, art. 6], el consentimiento de niños (mínimo 16 años, con la posibilidad de que los Estados bajen el umbral) [1, art. 8], las obligaciones con encargados, que no pueden subcontratar sin autorización del responsable [1, art. 28], y la notificación de brechas a la autoridad en 72 horas cuando hay riesgo [1, art. 33].

### 1.2 Argentina: Ley 25.326 y criterios de la AAIP

La ley exige informar de forma expresa y clara, antes de recabar los datos [2, art. 6]:

- finalidad y destinatarios o clase de destinatarios
- existencia del archivo o base, y identidad y domicilio del responsable
- carácter obligatorio o facultativo de las respuestas
- consecuencias de dar los datos, de negarse o de que sean inexactos
- posibilidad de ejercer acceso, rectificación y supresión

Puntos que disparan contenido en la política:

- Consentimiento: libre, expreso e informado, por escrito o medio equivalente, destacado si se presta junto con otras declaraciones [2, art. 5.1]. Tiene excepciones, entre ellas datos que derivan de una relación contractual y son necesarios para su cumplimiento [2, art. 5.2].
- Calidad: datos adecuados, pertinentes y no excesivos; no se pueden usar para fines incompatibles [2, art. 4].
- Cesión: solo con interés legítimo de cedente y cesionario y consentimiento previo, revocable, informando la finalidad e identificando al cesionario [2, art. 11].
- Transferencia internacional: prohibida hacia países sin nivel de protección adecuado, salvo excepciones taxativas [2, art. 12]. La AAIP publica la lista de países adecuados (UE y EEE, Reino Unido, Suiza, Uruguay, Canadá en su sector privado y otros) y explica que un proveedor de nube en el exterior es un caso típico de transferencia [3]. Los Estados Unidos no figuran en el fragmento de la lista que se alcanzó a leer, por lo que un proveedor estadounidense requiere un instrumento adicional; la página de la AAIP menciona cláusulas modelo [3]. La Disposición 60-E/2016 aprobó modelos de contrato para estas transferencias [4] [secundaria sobre el detalle].
- Seguridad y confidencialidad: medidas técnicas y organizativas para evitar adulteración, pérdida, consulta o tratamiento no autorizado [2, art. 9]; deber de secreto de quien interviene en el tratamiento [2, art. 10].
- Derechos: acceso en 10 días corridos desde la intimación, gratuito a intervalos no menores a seis meses [2, art. 14]; rectificación, actualización o supresión en 5 días hábiles [2, art. 16]. La AAIP repite esos plazos y explica el camino de la denuncia y del hábeas data [5].
- Registro: las bases privadas destinadas a dar informes deben inscribirse y declarar, entre otros datos, el tiempo de conservación y los medios de seguridad [2, art. 21]. La AAIP mantiene un Registro Nacional de Bases de Datos Personales donde se consulta el contacto del responsable [5].
- Autoridad: la AAIP es el órgano de control y recibe denuncias; la política debería mencionarla [2, art. 29; 6].
- Criterio de la AAIP sobre la política en sí: leerla debería llevar unos cinco minutos y decir qué se hace con los datos, la finalidad, quién es el responsable, cómo se protegen, con qué empresas se comparten y cuál es el canal para ejercer acceso, rectificación, actualización y supresión [6].
- La Resolución 4/2019 aprueba criterios orientadores de observancia obligatoria (por ejemplo sobre videovigilancia y derecho de acceso) [7]. No se leyó su anexo completo.
- Los derechos "ARCO" en Argentina se nombran como acceso, rectificación, actualización y supresión; la oposición aparece en los textos de las empresas pero no como derecho autónomo en la ley que se leyó [2] [5].

### 1.3 LGPD (Brasil), a grandes rasgos

La copia leída es el texto de 2018 alojado en un sitio de gobierno federal; la página de Planalto no se pudo leer [8]. Puede no incluir reformas posteriores.

- Bases legales (art. 7): consentimiento, obligación legal, ejecución de contrato, interés legítimo, protección del crédito, entre otras diez [8].
- Información (art. 9): acceso facilitado, claro, adecuado y ostensivo sobre finalidad específica, forma y duración del tratamiento, identificación y contacto del controlador, uso compartido de datos y su finalidad, responsabilidades de los agentes y derechos del titular con mención explícita al art. 18 [8].
- Derechos (art. 18): confirmación, acceso, corrección, anonimización o eliminación, portabilidad, información sobre con quién se compartió, información sobre la negativa a consentir y revocación [8].
- Menores (art. 14): tratamiento en su mejor interés; para niños, consentimiento específico y destacado de uno de los padres, y publicar qué datos se recogen y cómo ejercer derechos [8].
- Transferencia internacional (art. 33): permitida con país adecuado, cláusulas contractuales, normas corporativas, sellos, o consentimiento específico y destacado, entre otros [8].
- Encargado (art. 41): identidad y contacto publicados de forma clara, preferentemente en el sitio del controlador [8].
- Incidentes (art. 48): comunicación a la autoridad y a los titulares con un contenido mínimo [8].

### 1.4 CCPA y CPRA, a grandes rasgos

- La CPRA modificó la CCPA y no creó una ley aparte; rige desde el 1 de enero de 2023 [9].
- Aviso al momento de la recolección: categorías de información personal y fines, si se vende o comparte, categorías de información sensible y sus fines, y el plazo de conservación de cada categoría o los criterios para fijarlo [10, 1798.100(a)].
- Recolección, uso, retención y compartición deben ser razonablemente necesarios y proporcionales [10, 1798.100(c)].
- Contratos con terceros, proveedores de servicios y contratistas con propósitos limitados y especificados [10, 1798.100(d)].
- Medidas de seguridad razonables [10, 1798.100(e)].
- Derechos del consumidor de California: conocer, borrar, corregir, optar por que no se venda ni comparta su información y limitar el uso de la información sensible; sin discriminación por ejercerlos [9].
- El texto detallado de la política en línea (reglamento de la agencia) y los umbrales de aplicación no se pudieron leer en esta ronda; no se afirman acá.

### 1.5 Tabla de contenidos mínimos por norma

| Contenido | GDPR (arts. 13 y 14) | Ley 25.326 (art. 6 y concordantes) | LGPD (art. 9) | CCPA y CPRA (1798.100) |
| --- | --- | --- | --- | --- |
| Identidad y contacto del responsable | Sí | Sí, con domicilio | Sí | Implícito en el canal de solicitudes, no leído en detalle |
| Contacto del DPO o encargado | Si existe | No lo exige | Sí (art. 41) | No |
| Categorías de datos | Sí en art. 14; en art. 13 se deducen de los fines | Se informa la finalidad y el carácter de las respuestas | Sí, vía finalidad específica | Sí |
| Finalidades | Sí | Sí | Sí | Sí |
| Base jurídica | Sí | Consentimiento como regla, con excepciones | Sí (art. 7) | No, pero exige limitar a lo necesario y proporcional |
| Destinatarios | Sí | Sí | Sí, uso compartido | Si se vende o comparte, y contratos con terceros |
| Transferencias internacionales | Sí, con garantías | Prohibidas sin adecuación, salvo excepciones | Sí (art. 33) | No específico |
| Plazo de conservación | Sí, o criterios | En el registro de la base (art. 21) | Duración del tratamiento | Sí, por categoría |
| Derechos | Sí, lista completa | Acceso, rectificación, supresión | Sí (art. 18) | Sí |
| Retirar consentimiento | Sí | Cesión revocable (art. 11.2) | Sí | Opt-out de venta o compartición |
| Reclamo ante la autoridad | Sí | AAIP | Autoridad nacional (art. 18 §1) | Fiscal General o agencia de California [9] |
| Decisiones automatizadas y perfiles | Sí | Limitación del art. 20 | No leído | No leído |
| Obligatoriedad de dar los datos | Sí | Sí | Cuando es condición del servicio, con destaque (art. 9 §3) | No |
| Menores | Art. 8 y art. 12 (lenguaje) | No tiene un artículo específico en el texto leído | Art. 14 | No leído |

### 1.6 Qué datos del código disparan cada obligación

Esta tabla es criterio de diseño para la skill. Las obligaciones legales se citan; la conexión con el código es [opinión].

| Qué aparece en el código | Qué hay que decir en la política | Obligación de fondo |
| --- | --- | --- |
| Dirección IP en logs, rate limiting o analítica | Que se trata, para qué (seguridad, antifraude) y cuánto se conserva | La IP es un dato personal: se informa categoría, fin y plazo [1, arts. 13 y 14] [secundaria sobre la calificación de la IP; la ley argentina define dato personal como información referida a personas determinadas o determinables [2, art. 2]] |
| Cookies o almacenamiento local (localStorage, sessionStorage, IndexedDB) | Lista por finalidad (necesarias, funcionales, analítica, publicidad), duración y cómo desactivarlas | Transparencia y, para las no necesarias, consentimiento previo en la UE [1, art. 6.1.a] |
| Tokens OAuth y datos del proveedor de identidad (Google, GitHub, Apple) | Qué scopes se piden, qué se guarda (correo, nombre, avatar) y que los datos vienen de un tercero | Fuente de los datos [1, art. 14.2.f] |
| Tokens de acceso o refresh guardados en base | Que se almacenan, para qué, y cómo se revocan | Seguridad y minimización [2, arts. 4 y 9]; el OWASP pide no registrar tokens en logs [11] |
| Analítica (Google Analytics, Plausible, Mixpanel, PostHog) | Nombre del proveedor, qué mide, si hay transferencia a otro país, cómo optar por salir | Destinatarios y transferencias [1, art. 13.1.e y f] |
| Errores con Sentry u otro rastreador | Que los errores pueden incluir IP, identificador de usuario y contexto de la solicitud; proveedor y región | Destinatarios, transferencia, plazo [1, art. 13] |
| Subprocesadores (nube, correo, pagos, SMS, IA) | Lista nominal o por categorías con finalidad y país | Destinatarios [1, art. 13.1.e]; contratos [10, 1798.100(d)]; cesión con identificación del cesionario [2, art. 11.1] |
| Campos de fecha de nacimiento, edad, o verificación de edad | Edad mínima y mecanismo de autorización de adultos | Niños [1, art. 8] [8, art. 14] |
| Servidores o buckets fuera de Argentina | País, mecanismo (adecuación, cláusulas modelo) y consentimiento si corresponde | Transferencia internacional [2, art. 12] [3] |
| Campos de borrado, soft delete, jobs de limpieza, TTL, retención de logs | Plazos reales por categoría | Plazo de conservación [1, art. 13.2.a] [10, 1798.100(a)(3)] |
| Endpoints de exportación o borrado de cuenta | Cómo se ejerce cada derecho desde la app | Derechos [1, arts. 12 a 22] [2, arts. 14 y 16] |
| Perfilado, scoring, recomendaciones, modelos de IA con datos de usuarios | Que existe, la lógica general y la posibilidad de oponerse | Decisiones automatizadas [1, art. 13.2.f] [2, art. 20] |
| Datos de pago, documento de identidad, biometría, geolocalización precisa | Marcarlos como categoría aparte con su base | Categorías especiales y sensibles [1, art. 9, no leído en detalle] [2, art. 7] [10, definición en [9]] |
| Mensajes entre usuarios, contenido generado | Quién lo ve, cuánto se conserva | Finalidad y cesión [2, arts. 4 y 11] |

## 2. Política de seguridad

Hay dos documentos distintos que la gente llama "política de seguridad". Conviene no mezclarlos.

| | Política de seguridad de la web | SECURITY.md |
| --- | --- | --- |
| Lector | Usuario final, cliente, auditor | Investigador de seguridad o persona que encontró una falla |
| Pregunta que responde | "¿Cómo protegen mis datos?" | "¿Cómo les aviso de una vulnerabilidad?" |
| Contenido | Controles que el usuario puede leer: cifrado en tránsito, contraseñas, sesiones, 2FA, respaldo, respuesta a incidentes, notificación de brechas | Versiones soportadas, canal de reporte, qué incluir, plazos de respuesta, divulgación coordinada, puerto seguro |
| Dónde vive | Una página de la app (por ejemplo /seguridad) | Raíz, docs o .github del repositorio [12]; opcionalmente /.well-known/security.txt [13] |
| Riesgo si se escribe mal | Prometer controles que el código no tiene (ver sección 3) | Un canal que nadie lee |

Es una distinción propia del trabajo [opinión]; el OWASP la sostiene de hecho al tratar la divulgación como un proceso con contacto, guía de reporte y comunicación, separado de los controles técnicos [14].

### 2.1 SECURITY.md según GitHub Docs

- Ubicación: raíz del repositorio, carpeta docs o carpeta .github [12] (la versión actual de la página de GitHub explica solo el flujo de creación desde la pestaña "Security and quality"; la ubicación está en la versión previa de la misma página y en la documentación de GitHub Enterprise Server) [12].
- Qué debe tener según GitHub: información sobre las versiones soportadas y cómo reportar una vulnerabilidad [15].
- Qué muestra la interfaz: desde la pestaña de seguridad del repositorio se llega a "Security policy"; si el repositorio tiene política, se muestra por encima del formulario de reporte privado para que quien reporta lea la guía antes de enviar [15] [16].
- Reporte privado de vulnerabilidades (private vulnerability reporting): lo habilitan propietarios y administradores de repositorios públicos; cualquiera puede reportar; el formulario pide por defecto resumen, detalles, prueba de concepto e impacto; el reportante queda como colaborador y con crédito pendiente en el advisory [16]. Es independiente de SECURITY.md: solo se puede reportar así donde está habilitado [16].
- Si no hay reporte privado ni política: quien reporta puede abrir un issue pidiendo un contacto de seguridad, sin incluir detalles del fallo porque el issue es público [17].
- Buenas prácticas para mantenedores según GitHub: indicar con claridad dónde y cómo recibir reportes, acusar recibo rápido, involucrar a quien reporta, dar crédito, publicar un advisory y marcar los releases que corrigen seguridad [17].

### 2.2 security.txt (RFC 9116)

- Ubicación: /.well-known/security.txt por HTTPS, con Content-Type text/plain y utf-8; la ubicación en la raíz se admite por compatibilidad y gana la de .well-known si existen ambas [13, sec. 3].
- Campos obligatorios: Contact (puede repetirse, en orden de preferencia, con URI mailto, tel o https) y Expires (una sola vez, recomendado menos de un año adelante) [13, secs. 2.5.3 y 2.5.5].
- Campos opcionales: Acknowledgments, Canonical, Encryption, Hiring, Policy, Preferred-Languages [13, sec. 2.5].
- Firma OpenPGP recomendada [13, sec. 2.3].
- Alcance: solo aplica al dominio desde el que se sirve [13, sec. 3.1].
- Advertencia: publicar el archivo no implica permiso para hacer pruebas [13, sec. 5.5 en el índice; no se leyó el cuerpo de la sección].
- No reemplaza una política de divulgación; la complementa [13, sec. 1.1].

### 2.3 OWASP

- Cheat sheet de divulgación de vulnerabilidades [14]. Para organizaciones: dar un método claro y seguro de reporte, establecer alcance y términos, responder en plazos razonables, comunicar abiertamente, no amenazar con acciones legales, pedir CVE cuando corresponda, publicar advisories y changelogs, y ofrecer crédito o recompensa. Canales sugeridos: contacto de seguridad dedicado, correo security@, security.txt, issue tracker o programa de recompensas. Guía para quien reporta: qué información incluir, redactar datos personales, y plazos acordados. Un advisory debe tener como mínimo resumen e impacto, versiones vulnerables, versiones corregidas, condiciones en las que aplica, mitigaciones y CVE si existe.
- Plazos de referencia: la política de Google Project Zero da 90 días al fabricante para publicar un parche y publica los detalles técnicos 30 días después; con excepciones para fallas explotadas en producción [14].
- Safe harbor: el cheat sheet indica que una política de puerto seguro permite hacer pruebas dentro del alcance y de las reglas, que hay que definirla con asesoría legal y no con el cheat sheet, y remite a disclose.io para ejemplos [14].
- Cheat sheet de protección de la privacidad del usuario: cifrado fuerte en tránsito y almacenamiento, hash de contraseñas con factor de trabajo creciente, HSTS, invalidación remota de sesiones y honestidad con el usuario cuando la aplicación no puede garantizar algo [18]. El apartado "Honesty & Transparency" sostiene que si la aplicación no puede dar garantías, hay que decirlo con claridad.
- Cheat sheet de logging: no registrar directamente tokens de acceso, identificadores de sesión, contraseñas, cadenas de conexión, claves, datos de pago ni información personal sensible; tampoco información que el usuario no consintió que se recolecte [11].
- ASVS 5.0: el capítulo V14 (Data Protection) pide documentar los requisitos de protección por nivel de clasificación de los datos, y cubre datos sensibles que no se envían a partes no confiables y datos sensibles en el cliente (caché y almacenamiento del navegador) [19] [secundaria sobre los números de requisito citados en los resultados de búsqueda; no se leyó el capítulo completo].

### 2.4 Divulgación coordinada: plazos y puerto seguro

- Modelo: el reporte inicial es privado y los detalles completos se publican cuando hay parche, a veces con una demora [20] [14].
- Plazo típico del reportante: 90 días (Project Zero) [14]. El propio OWASP aclara que las políticas varían.
- GitHub señala que es aceptable que quien reporta divulgue después de un tiempo si intentó contactar y no tuvo respuesta, o si le pidieron esperar demasiado [20].
- Tiempos de respuesta del lado de la organización: el OWASP recomienda establecer cronograma de acuse, triage y corrección, sin fijar números [14]. Un caso real, Mercado Libre, publica sus métricas: 16 horas a primera respuesta, un día a triage y tres días a recompensa en promedio, y recomienda incluir un SLA autoimpuesto en la política [21].
- Puerto seguro: no hay un texto único. La recomendación es explicitar que las pruebas dentro del alcance no motivarán acciones legales, y revisarlo con un abogado [14].

## 3. Errores comunes al redactarlas

Con fuente primaria:

1. Prometer más de lo que se hace. El OWASP pide que si la aplicación no puede dar una garantía o evitar un mal uso de información sensible, se diga con claridad al usuario [18]. La ley argentina exige medidas "técnicas y organizativas que resulten necesarias" y prohíbe registrar datos en archivos sin condiciones de integridad y seguridad [2, art. 9]; una política que promete cifrado o auditorías inexistentes contradice la información veraz que exige el artículo 4 (datos ciertos) y la transparencia del GDPR [1, art. 12.1].
2. No decir plazos de conservación. Tanto el GDPR como la CCPA piden el plazo o los criterios [1, art. 13.2.a] [10, 1798.100(a)(3)].
3. No identificar a los destinatarios. El GDPR pide destinatarios o categorías [1, art. 13.1.e]; la ley argentina pide que la cesión identifique al cesionario o dé elementos para hacerlo [2, art. 11.1].
4. Olvidar las transferencias internacionales cuando se usa nube, analítica o correo en el exterior [2, art. 12] [3].
5. Un canal de derechos que no existe: la AAIP dice que debe estar definido en la política [6].
6. Consentimiento global por aceptar términos. La ley argentina pide que el consentimiento dado junto con otras declaraciones figure expresa y destacadamente [2, art. 5.1]; la LGPD declara nulo el consentimiento si la información fue engañosa, abusiva o no se presentó con transparencia [8, art. 9 §1].
7. Lenguaje no claro. El GDPR exige lenguaje claro y sencillo [1, art. 12.1]; la AAIP habla de unos cinco minutos de lectura [6].
8. Dejar el SECURITY.md sin un canal real, o con un correo sin monitorear. GitHub advierte que sin información clara los investigadores acaban sacando correos del historial de git o divulgando de forma pública [20].
9. security.txt con Expires vencido: el RFC trata el dato vencido como no confiable [13, secs. 2.5.5 y 5.3 en el índice].
10. Nunca actualizar la política cuando cambia el código. La Ley 25.326 exige informar la finalidad "previamente" y el GDPR exige informar antes de un fin nuevo [2, art. 6] [1, art. 13.3].

Sin fuente primaria específica, marcados como opinión:

11. Copiar una plantilla genérica sin adaptarla a la app (plantillas con "cookies de publicidad" cuando no hay ninguna) [opinión]. Es un caso particular del punto 1: el contenido debe describir tratamientos reales.
12. Listar a los subprocesadores solo como "terceros de confianza" sin nombre ni categoría [opinión], aunque el criterio de categorías es admitido por el GDPR [1, art. 13.1.e].
13. Declarar cumplimiento de GDPR, LGPD o CCPA sin que nadie lo haya evaluado [opinión].
14. En SECURITY.md, prometer plazos de respuesta que el equipo no puede cumplir [opinión]; el caso de Mercado Libre muestra que el SLA se mide y se publica [21].

## 4. Qué NO se puede afirmar por leer el código

La skill debe dejar estos puntos como pregunta abierta para el titular, no como afirmación. Es criterio propio [opinión], salvo donde se cita.

- Cumplimiento legal. Leer el código muestra qué se hace con los datos, no si hay base legal válida, consentimiento válido ni registro en la AAIP. Quién es el responsable legal, su CUIT y su domicilio no están en el código.
- Quién es el DPO o encargado y cuál es el canal de contacto. Hay que preguntarlo.
- Retención real. El código muestra jobs de borrado o TTL, pero no qué pasa en backups, réplicas, logs de infraestructura, data warehouses ni en los sistemas de los subprocesadores. Uber y PedidosYa, por ejemplo, aclaran en sus políticas qué sobrevive al borrado (ver ejemplos.md).
- Controles de infraestructura: cifrado en reposo del disco, gestión de claves, segmentación de red, acceso del personal, logs de acceso administrativos, monitoreo, respuesta a incidentes, pruebas de intrusión. Salvo que el repositorio incluya infraestructura como código, esto es opaco.
- Región real de los datos y de los proveedores, y los contratos con ellos (cláusulas modelo, acuerdos de procesamiento de datos).
- Si un tercero usa los datos para entrenar modelos o fines propios: depende del contrato y de la configuración de su panel.
- Cookies y scripts cargados dinámicamente por un gestor de etiquetas (por ejemplo Google Tag Manager): el código no muestra qué terminan cargando.
- Existencia de SLAs de respuesta a vulnerabilidades, quién monitorea el correo de seguridad, y si habrá puerto seguro: decisión del titular, con asesoría legal [14].
- Edad de los usuarios y si hay menores: el código muestra si se pregunta la edad, no quién se registra.
- Qué versiones reciben parches: lo define el titular.

## Fuentes

Primarias:

1. Reglamento (UE) 2016/679 (GDPR), texto en español, EUR-Lex. https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=CELEX:32016R0679
2. Ley 25.326 de Protección de los Datos Personales, texto original, InfoLEG. https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/norma.htm
3. AAIP, Transferencias internacionales. https://argentina.gob.ar/transferencias-internacionales
4. Disposición 60-E/2016, InfoLEG (solo se vio en resultados de búsqueda; no se leyó el texto). https://servicios.infoleg.gob.ar/infolegInternet/anexos/265000-269999/267922/norma.htm
5. AAIP, Conocé tus derechos respecto a tus datos personales. https://argentina.gob.ar/aaip/datospersonales/derechos
6. AAIP, Recomendaciones para proteger datos personales en Internet (2024-01-26). https://argentina.gob.ar/noticias/recomendaciones-de-la-aaip-para-proteger-datos-personales-en-internet
7. AAIP, Resolución 4/2019, criterios orientadores (solo el resumen del resultado de búsqueda). https://argentina.gob.ar/normativa/nacional/norma-318874/texto
8. Lei 13.709/2018 (LGPD), copia en gov.br de la Imprensa Nacional (la página de Planalto devolvió contenido ajeno). https://www.gov.br/cnen/pt-br/acesso-a-informacao/ouvidoria/LEINo13.709DE14DEAGOSTODE2018ImprensaNacional.pdf
9. Oficina del Fiscal General de California, CCPA, actualizada el 28 de agosto de 2026. https://oag.ca.gov/privacy/ccpa
10. California Civil Code 1798.100, Legislatura de California. https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100
11. OWASP Logging Cheat Sheet, sección "Data to exclude". https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
12. GitHub Docs, Adding a security policy to your repository (versión actual y versión previa con la ubicación en root, docs o .github, vista en el resultado de búsqueda). https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy y https://docs.github.com/en/code-security/security-advisories/adding-a-security-policy-to-your-repository
13. RFC 9116, A File Format to Aid in Security Vulnerability Disclosure. https://www.rfc-editor.org/rfc/rfc9116.txt
14. OWASP Vulnerability Disclosure Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html
15. GitHub Docs, GitHub security features (sección Security policy). https://docs.github.com/en/code-security/getting-started/github-security-features
16. GitHub Docs, Privately reporting a security vulnerability. https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability
17. GitHub Docs, Coordinated disclosure of security vulnerabilities (secciones Standard process y Best practices for maintainers). https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/coordinated-disclosure
18. OWASP User Privacy Protection Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html
19. OWASP ASVS, página del proyecto (versión estable 5.0.0) y capítulo V14 visto solo en resultados de búsqueda. https://asvs.owasp.org y https://github.com/OWASP/ASVS/blob/master/5.0/en/0x23-V14-Data-Protection.md
20. GitHub Docs, Coordinated disclosure (misma URL que 17, secciones sobre reportantes y modelo general).
21. HackerOne, blog "Mercado Libre's Journey to a Public Bug Bounty Program", 2023-11-28, firmado por el director de Application Security de Mercado Libre. Es fuente de la propia empresa alojada en el sitio del proveedor. https://www.hackerone.com/blog/mercado-libres-journey-public-bug-bounty-program

Páginas que no se pudieron leer o se leyeron solo en parte: Planalto (LGPD original), HackerOne de Mercado Libre y Uber (contenido dinámico), texto completo de la Disposición 60-E/2016 y de la Resolución 4/2019, reglamento de la CCPA sobre política en línea, capítulo V14 de ASVS, cuerpo de las secciones 5.x del RFC 9116.

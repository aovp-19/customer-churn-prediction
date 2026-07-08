const API_URL = "http://127.0.0.1:8000/predict";

const form = document.getElementById("churnForm");
const resultadoDiv = document.getElementById("resultado");
const resultadoBadge = document.getElementById("resultadoBadge");
const resultadoTitulo = document.getElementById("resultadoTitulo");
const resultadoDescripcion = document.getElementById("resultadoDescripcion");
const gaugeFill = document.getElementById("gaugeFill");
const gaugeNeedle = document.getElementById("gaugeNeedle");
const gaugeValue = document.getElementById("gaugeValue");
const recsList = document.getElementById("recsList");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const formData = new FormData(form);
  const datos = {};

  for (const [key, value] of formData.entries()) {
    if (["SeniorCitizen", "tenure"].includes(key)) {
      datos[key] = parseInt(value);
    } else if (["MonthlyCharges", "TotalCharges"].includes(key)) {
      datos[key] = parseFloat(value);
    } else {
      datos[key] = value;
    }
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    });

    if (!response.ok) {
      throw new Error("Error en la predicción. Verificá los datos ingresados.");
    }

    const resultado = await response.json();
    mostrarResultado(resultado, datos);

  } catch (error) {
    alert(error.message);
  }
});

function mostrarResultado(resultado, datosCliente) {
  const esChurn = resultado.prediccion === "Churn";
  const probabilidad = Math.round(resultado.probabilidad_churn * 100);

  resultadoDiv.classList.remove("d-none");

  // --- Gauge: la circunferencia del arco es 283 (radio 90, medio círculo) ---
  // stroke-dashoffset va de 283 (0% lleno) a 0 (100% lleno)
  const offset = 283 - (283 * probabilidad) / 100;
  gaugeFill.style.strokeDashoffset = offset;
  gaugeFill.style.stroke = esChurn ? "var(--amber)" : "var(--teal)";

  // La aguja rota de -90deg (0%) a +90deg (100%) sobre su punto de anclaje
  const rotacion = -90 + (180 * probabilidad) / 100;
  gaugeNeedle.style.transform = `rotate(${rotacion}deg)`;

  gaugeValue.textContent = probabilidad + "%";

  // --- Texto y badge ---
  resultadoBadge.textContent = esChurn ? "Riesgo detectado" : "Cliente estable";
  resultadoBadge.className = "result-badge " + (esChurn ? "risk" : "safe");

  resultadoTitulo.textContent = esChurn
    ? "Este cliente tiene alta probabilidad de abandonar"
    : "Este cliente probablemente permanezca";

  resultadoDescripcion.textContent = esChurn
    ? "El modelo identificó un patrón de riesgo similar al de clientes que históricamente terminaron cancelando el servicio."
    : "El perfil de este cliente se asemeja al de clientes que históricamente se mantuvieron activos.";

  // --- Recomendaciones dinámicas, basadas en los factores de riesgo presentes ---
  recsList.innerHTML = "";
  const recomendaciones = generarRecomendaciones(datosCliente, esChurn);

  recomendaciones.forEach(texto => {
    const li = document.createElement("li");
    li.textContent = texto;
    recsList.appendChild(li);
  });

  resultadoDiv.scrollIntoView({ behavior: "smooth", block: "center" });
}

// Motor simple de recomendaciones: revisa qué factores de riesgo conocidos
// (identificados durante el EDA) están presentes en este cliente específico,
// y sugiere una acción de retención concreta para cada uno.
function generarRecomendaciones(datos, esChurn) {
  const recs = [];

  if (!esChurn) {
    recs.push("No se detectan señales de riesgo relevantes. Es un buen candidato para ofertas de upgrade o venta cruzada de servicios adicionales.");
    return recs;
  }

  if (datos.Contract === "Month-to-month") {
    recs.push("Ofrecer un descuento por migrar a un contrato anual o de dos años: los contratos largos están fuertemente asociados a menor abandono.");
  }

  if (datos.PaymentMethod === "Electronic check") {
    recs.push("Incentivar el cambio a pago automático (tarjeta o transferencia): el pago por cheque electrónico se asocia a mayor tasa de churn.");
  }

  if (datos.tenure < 6) {
    recs.push("Activar un seguimiento proactivo de bienvenida: los clientes con menos de 6 meses de antigüedad tienen el riesgo más alto de abandono temprano.");
  }

  if (datos.InternetService === "Fiber optic" && (datos.OnlineSecurity === "No" || datos.TechSupport === "No")) {
    recs.push("Ofrecer en bundle los servicios de Seguridad en línea y Soporte técnico: los clientes de fibra óptica sin estos servicios muestran mayor abandono.");
  }

  if (parseFloat(datos.MonthlyCharges) > 70 && datos.tenure < 12) {
    recs.push("Evaluar una oferta de retención personalizada: el cargo mensual es alto en relación a la antigüedad del cliente, lo cual eleva la percepción de costo/beneficio.");
  }

  if (recs.length === 0) {
    recs.push("Contactar proactivamente para entender su nivel de satisfacción: el modelo detecta riesgo, pero no se identifican factores específicos conocidos en este perfil.");
  }

  return recs;
}
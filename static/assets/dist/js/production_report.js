const csrfToken = document.cookie
  .split(";")
  .find((c) => c.trim().startsWith("csrftoken="))
  ?.split("=")[1];

const reportUrl = "/product-gestion/production/month-cumulative-report/";
const entityUrl = "/product-gestion/entity/";
const classificationUrl = "/product-gestion/classification/";
const productUrl = "/product-gestion/product/";

const MONTH_NAMES = [
  "enero",
  "febrero",
  "marzo",
  "abril",
  "mayo",
  "junio",
  "julio",
  "agosto",
  "septiembre",
  "octubre",
  "noviembre",
  "diciembre",
];

const MONTH_LABELS = [
  "Enero",
  "Febrero",
  "Marzo",
  "Abril",
  "Mayo",
  "Junio",
  "Julio",
  "Agosto",
  "Septiembre",
  "Octubre",
  "Noviembre",
  "Diciembre",
];

function fmt(n) {
  const value = parseFloat(n) || 0;
  return value % 1 === 0
    ? value.toLocaleString("es-ES")
    : value.toLocaleString("es-ES", { maximumFractionDigits: 2 });
}

function pctBadge(pct) {
  if (pct >= 100) {
    return `<span class="badge badge-success">${fmt(pct)}%</span>`;
  }
  if (pct >= 70) {
    return `<span class="badge badge-warning">${fmt(pct)}%</span>`;
  }
  return `<span class="badge badge-danger">${fmt(pct)}%</span>`;
}

function faltanteCell(faltante) {
  if (faltante < 0) {
    return `<span class="badge badge-success">+${fmt(Math.abs(faltante))}</span>`;
  }
  if (faltante > 0) {
    return `<span class="badge badge-danger">${fmt(faltante)}</span>`;
  }
  return `<span class="text-muted">${fmt(faltante)}</span>`;
}

function sumRange(values, months) {
  let total = 0;
  months.forEach((m) => {
    total += parseFloat(values[MONTH_NAMES[m - 1]] || 0) || 0;
  });
  return total;
}

function pct(real, plan) {
  if (plan > 0) {
    return (real / plan) * 100;
  }
  return real > 0 ? 100 : 0;
}

function buildTable(rows) {
  const table = $("#tabla-reporte").DataTable();
  table.clear();
  table.rows.add(rows).draw();
}

function initTable() {
  $("#tabla-reporte").DataTable({
    responsive: true,
    pageLength: 25,
    dom: '<"top"l>Bfrtip',
    buttons: [
      {
        extend: "excel",
        text: "Excel",
        exportOptions: {
          columns: ":visible",
        },
      },
      {
        extend: "pdf",
        text: "PDF",
        exportOptions: {
          columns: ":visible",
        },
      },
      {
        extend: "print",
        text: "Imprimir",
        exportOptions: {
          columns: ":visible",
        },
      },
      {
        extend: "colvis",
        text: "Columnas",
      },
    ],
    columns: [
      { data: "ueb", title: "UEB" },
      { data: "classification", title: "Clasificación" },
      { data: "product", title: "Producto" },
      { data: "m_plan", title: "Plan (Mes)" },
      { data: "m_real", title: "Real (Mes)" },
      { data: "m_faltante", title: "Faltante (Mes)" },
      { data: "m_pct", title: "% Cumpl." },
      { data: "a_plan", title: "Plan (Acum)" },
      { data: "a_real", title: "Real (Acum)" },
      { data: "a_faltante", title: "Faltante (Acum)" },
      { data: "a_pct", title: "% Cumpl." },
    ],
    ordering: false,
  });
}

function generarReporte() {
  const year = $("#year").val();
  const month = parseInt($("#month").val(), 10);
  const ueb = $("#ueb").val();
  const classification = $("#classification").val();
  const product = $("#product").val();

  if (!year) {
    Swal.fire("Aviso", "Debe indicar el año", "warning");
    return;
  }

  const params = {
    year: year,
  };
  if (ueb) {
    params["plan__ueb"] = ueb;
  }
  if (classification) {
    params["product__classification"] = classification;
  }
  if (product) {
    params["product"] = product;
  }

  const monthName = MONTH_NAMES[month - 1];
  const monthsToSum = Array.from({ length: month }, (_, i) => i + 1);

  axios
    .get(reportUrl, { params })
    .then((res) => {
      const data = res.data;
      const rows = [];

      (data.report || []).forEach((uebData) => {
        (uebData.classifications || []).forEach((cls) => {
          (cls.products || []).forEach((prod) => {
            const monthReal = parseFloat(prod.monthly_production[monthName] || 0) || 0;
            const monthPlan = parseFloat(cls.plan_monthly_totals[monthName] || 0) || 0;
            const monthFaltante = monthPlan - monthReal;
            const monthPct = pct(monthReal, monthPlan);

            const annualReal = sumRange(prod.monthly_production, monthsToSum);
            const annualPlan = sumRange(cls.plan_monthly_totals, monthsToSum);
            const annualFaltante = annualPlan - annualReal;
            const annualPct = pct(annualReal, annualPlan);

            rows.push({
              ueb: uebData.ueb_name,
              classification: cls.classification_name,
              product: prod.product_name,
              m_plan: fmt(monthPlan),
              m_real: fmt(monthReal),
              m_faltante: faltanteCell(monthFaltante),
              m_pct: pctBadge(monthPct),
              a_plan: fmt(annualPlan),
              a_real: fmt(annualReal),
              a_faltante: faltanteCell(annualFaltante),
              a_pct: pctBadge(annualPct),
            });
          });
        });
      });

      if (rows.length === 0) {
        $("#reporte-titulo").text(
          "Sin datos para " + MONTH_LABELS[month - 1] + " de " + year
        );
      } else {
        $("#reporte-titulo").text(
          "Mes: " + MONTH_LABELS[month - 1] + " de " + year + "  ·  Acumulado: enero – " + MONTH_LABELS[month - 1]
        );
      }

      buildTable(rows);
    })
    .catch((error) => {
      Swal.fire("Error", "No se pudo generar el reporte", "error");
      console.error(error);
    });
}

function poblarMes() {
  const $month = $("#month");
  MONTH_LABELS.forEach((label, index) => {
    $month.append(new Option(label, index + 1));
  });
}

let clasificaciones = [];
let productos = [];

function getDescendantIds(classificationId) {
  const ids = [classificationId];
  const stack = [classificationId];
  while (stack.length) {
    const current = stack.pop();
    clasificaciones.forEach((c) => {
      if (c.parent === current && !ids.includes(c.id)) {
        ids.push(c.id);
        stack.push(c.id);
      }
    });
  }
  return ids;
}

function filtrarProductos() {
  const classificationId = $("#classification").val();
  const ids = classificationId
    ? getDescendantIds(parseInt(classificationId, 10))
    : null;
  const $product = $("#product");
  const current = $product.val();

  $product.empty();
  $product.append(new Option("Todos", ""));
  productos.forEach((p) => {
    if (!ids || ids.includes(p.classification)) {
      $product.append(new Option(p.name, p.id));
    }
  });

  if (!ids || ids.includes(parseInt(current, 10))) {
    $product.val(current);
  } else {
    $product.val("");
  }
  $product.trigger("change");
}

function poblarListas() {
  axios.get(entityUrl).then((res) => {
    (res.data.results || []).forEach((el) => {
      $("#ueb").append(new Option(el.name, el.id));
    });
  });

  axios.get(classificationUrl).then((res) => {
    clasificaciones = (res.data.results || []).map((el) => ({
      id: el.id,
      parent: el.parent,
    }));
    clasificaciones.forEach((el) => {
      const found = (res.data.results || []).find((c) => c.id === el.id);
      $("#classification").append(new Option(found.name, found.id));
    });
  });

  axios.get(productUrl).then((res) => {
    productos = (res.data.results || []).map((el) => ({
      id: el.id,
      name: el.name,
      classification: el.classification.id,
    }));
    productos.forEach((el) => {
      $("#product").append(new Option(el.name, el.id));
    });
  });
}

$(document).ready(function () {
  $("#year").val(new Date().getFullYear());
  const currentMonth = new Date().getMonth() + 1;
  initTable();
  poblarMes();
  $("#month").val(currentMonth <= 12 ? currentMonth : 12).trigger("change");

  $(".select2").select2({
    theme: "bootstrap4",
  });

  $("#classification").on("change", function () {
    filtrarProductos();
  });

  $("#form-reporte").on("submit", function (e) {
    e.preventDefault();
    generarReporte();
  });
});

$(function () {
  poblarListas();
});
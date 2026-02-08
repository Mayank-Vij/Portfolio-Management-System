const backendURL = "http://127.0.0.1:8000";
let liveChart;

// Toast helper
function showToast(msg){
  const toast=document.getElementById("toast");
  toast.textContent=msg;
  toast.classList.add("show");
  setTimeout(()=>toast.classList.remove("show"),3000);
}

// Section switcher
function showSection(id){
  document.querySelectorAll('.section').forEach(sec=>sec.classList.add('hidden'));
  const target=document.getElementById(id);
  target.classList.remove('hidden');
  target.classList.add('active');
  showToast(`Switched to ${id.charAt(0).toUpperCase()+id.slice(1)}`);
}

// --------------------- LIVE PRICES ---------------------
async function loadLivePrices(auto = false) {
    const div = document.getElementById("livePricesResult");
    div.innerHTML = "<p class='loader'>Fetching Real-Time Prices...</p>";

    let tickers = ["INFY", "TCS", "RELIANCE", "SBIN", "HDFCBANK", "ICICIBANK"];

    const url = tickers.map(t => `tickers=${t}`).join("&");

    try {
        const res = await fetch(`${backendURL}/analytics/live-prices/?${url}`);
        const data = await res.json();

        div.innerHTML = data.live_prices.map(s => `
            <div class="stock-item">
                <b>${s.ticker}</b><br>
                ₹${s.price}
            </div>
        `).join('');

    } catch (e) {
        div.innerHTML = "<p>⚠️ Could not fetch live prices</p>";
    }

    if (!auto) {
        setTimeout(() => loadLivePrices(true), 30000);  // refresh every 30 sec
    }
}


// --------------------- PORTFOLIO ---------------------
async function calculatePortfolio(){
  const div=document.getElementById("portfolioResult");
  div.innerHTML="<p class='loader'>Calculating...</p>";
  const text=document.getElementById("portfolioData").value.trim();
  const lines=text.split("\n");const tickers=[],quantities=[];
  lines.forEach(l=>{const [t,q]=l.split(",");if(t&&q){tickers.push(t.trim());quantities.push(parseInt(q.trim()));}});
  try{
    const params=tickers.map(t=>`tickers=${t}`).join("&")+"&"+quantities.map(q=>`quantities=${q}`).join("&");
    const res=await fetch(`${backendURL}/analytics/portfolio-value/?${params}`);
    const data=await res.json();
    div.innerHTML=`<h3>Total Value: ₹${data.total_portfolio_value}</h3>`+
      data.details.map(i=>`<p>${i.ticker}: ${i.qty} × ₹${i.price?.toFixed(2)||'N/A'} = ₹${i.value?.toFixed(2)||'N/A'}</p>`).join('');
    showToast("Portfolio Calculated!");
  }catch{div.innerHTML="<p>Error.</p>";}
}

// --------------------- PREDICTION ---------------------
async function predictPrice(){
  const div=document.getElementById("predictionResult");
  div.innerHTML="<p class='loader'>Predicting...</p>";
  const ticker=document.getElementById("predictTicker").value.trim();
  try{
    const [predRes,sharpeRes]=await Promise.all([
      fetch(`${backendURL}/analytics/predict-price/?ticker=${ticker}`),
      fetch(`${backendURL}/analytics/sharpe-ratio/?ticker=${ticker}`)
    ]);
    const predData=await predRes.json();const sharpeData=await sharpeRes.json();
    div.innerHTML=`
      <h3>${ticker}</h3>
      <p><b>Last Close:</b> ₹${predData.last_close}</p>
      <p><b>Predicted Next Close:</b> ₹${predData.predicted_next_close}</p>
      <p><b>Confidence:</b> ${predData.confidence_percentage}%</p>
      <p><b>Sharpe Ratio:</b> ${sharpeData.sharpe_ratio}</p>`;
    showToast("Prediction ready!");
  }catch{div.innerHTML="<p>⚠️ Prediction failed.</p>";}
}

// --------------------- RISK ---------------------
async function analyzeRisk(){
  const div=document.getElementById("riskResult");
  div.innerHTML="<p class='loader'>Analyzing...</p>";
  const ticker=document.getElementById("riskTicker").value.trim();
  try{
    const [riskRes,metricsRes,anomRes]=await Promise.all([
      fetch(`${backendURL}/analytics/predict-risk/?ticker=${ticker}`),
      fetch(`${backendURL}/analytics/risk-metrics/?ticker=${ticker}`),
      fetch(`${backendURL}/analytics/anomalies/?ticker=${ticker}`)
    ]);
    const r=await riskRes.json(),m=await metricsRes.json(),a=await anomRes.json();
    div.innerHTML=`
      <p><b>Risk Level:</b> ${r.predicted_risk_level}</p>
      <p><b>Volatility:</b> ${r.recent_volatility}</p>
      <p><b>Std Dev:</b> ${m.standard_deviation}</p>
      <p><b>VaR 95%:</b> ${m.VaR_95}</p>
      <h4>Anomalies: ${a.anomalies_detected}</h4>`;
    showToast("Risk Analyzed");
  }catch{div.innerHTML="<p>Error analyzing risk.</p>";}
}

// --------------------- PCA ---------------------
async function runPCA(){
  const div=document.getElementById("pcaResult");
  div.innerHTML="<p class='loader'>Running PCA...</p>";
  const ticker=document.getElementById("pcaTicker").value.trim();
  try{
    const res=await fetch(`${backendURL}/analytics/pca-analysis/?ticker=${ticker}`);
    const data=await res.json();
    if(data.plot_path){
      div.innerHTML=`<img src='${backendURL}/plots/${ticker}_pca_variance.png' style='width:100%'>`;
      showToast("PCA Ready");
    }else div.innerHTML="<p>No plot.</p>";
  }catch{div.innerHTML="<p>PCA error.</p>";}
}

// --------------------- LEARNING ---------------------
async function openFinLearn(){
  const div=document.getElementById("learnCourses");
  div.innerHTML="<p class='loader'>Loading courses...</p>";
  try{
    const res=await fetch(`${backendURL}/finlearn/courses`);
    const data=await res.json();
    div.innerHTML=data.available_courses.map(c=>
      `<div class='card'>
        <h4>${c.title}</h4>
        <p>${c.description}</p>
        <p><i>${c.duration} | ${c.level}</i></p>
      </div>`
    ).join('');
    showToast("Courses Loaded");
  }catch{div.innerHTML="<p>Failed to load courses.</p>";}
}

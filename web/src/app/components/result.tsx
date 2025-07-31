import React from 'react';

// Data for the components
const valuationQueries = [
  { id: 'M1', complexity: 'Medium', text: "Which event had a greater impact on healthcare access: ’A’ or ’B’?" },
  { id: 'M2', complexity: 'Medium', text: "Compare the environmental and socio-economic impacts between ’A’ and ’B’." },
  { id: 'H1', complexity: 'High', text: "What mitigation measures were most effective during ’A’?" },
  { id: 'H2', complexity: 'High', text: "What logistical challenges affected evacuation efforts during ’B’?" },
];

const judgeScores = [
  { id: 'M1', kg: 9.3, rag: 7.5, llm: 4.5, kgiqd: 10.0 },
  { id: 'M2', kg: 8.0, rag: 9.0, llm: 6.0, kgiqd: 10.0 },
  { id: 'H1', kg: 9.4, rag: 9.7, llm: 3.8, kgiqd: 10.0 },
  { id: 'H2', kg: 7.0, rag: 9.0, llm: 5.0, kgiqd: 10.0 },
];

const evaluationCriteria = [
    { criterion: 'Factual Density & Specificity', weight: '60%' },
    { criterion: 'Efficiency & Clarity', weight: '20%' },
    { criterion: 'Relevance & Topical Alignment', weight: '20%' },
];


const Result = () => {
  return (
    <section className="font-sans p-6 md:p-8 w-full">
      <div className="w-full max-w-6xl mx-auto space-y-8">

        {/* Top Row: Queries and Method */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left Column: Reasoning Queries */}
          <div className="bg-white p-6 rounded-lg shadow-md h-full">
            <h3 className="text-xl font-bold text-gray-800 mb-1">Reasoning Queries</h3>
            <p className="text-sm text-gray-500 mb-4">’A’: 2015 Nepal Quake, ’B’: 2018 Kerala Floods</p>
            <ul className="space-y-3 text-sm">
              {valuationQueries.map(q => (
                <li key={q.id}><strong className="font-semibold text-gray-700">{q.id} ({q.complexity}):</strong> {q.text}</li>
              ))}
            </ul>
          </div>

          {/* Right Column: Evaluation Method */}
          <div className="bg-white p-6 rounded-lg shadow-md h-full">
            <h3 className="text-xl font-bold text-gray-800 mb-2">Evaluation Method</h3>
            <p className="text-sm text-gray-600 mb-4">
              We used a penalized LLM-as-Judge framework, randomizing outputs to avoid bias and rewarding high factual density.
            </p>
            <table className="w-full text-sm">
                <thead className="text-left">
                    <tr className="border-b">
                        <th className="pb-2 font-semibold">Scoring Criteria</th>
                        <th className="pb-2 font-semibold text-right">Weight</th>
                    </tr>
                </thead>
                <tbody>
                    {evaluationCriteria.map(c => (
                        <tr key={c.criterion} className="border-b last:border-none">
                            <td className="py-2 text-gray-700">{c.criterion}</td>
                            <td className="py-2 text-gray-700 text-right">{c.weight}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
          </div>
        </div>

        {/* Bottom Row: Performance Scores */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold text-gray-800 mb-1">Performance Scores</h3>
          <p className="text-sm text-gray-500 mb-4">KG-IQD consistently outperforms all baselines, achieving a perfect score on all queries.</p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-600">
              <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                  <th scope="col" className="px-4 py-3">Query ID</th>
                  <th scope="col" className="px-4 py-3 text-center">KG-Only</th>
                  <th scope="col" className="px-4 py-3 text-center">RQ-RAG</th>
                  <th scope="col" className="px-4 py-3 text-center">Base LLM</th>
                  <th scope="col" className="px-4 py-3 text-center">KG-IQD (Ours)</th>
                </tr>
              </thead>
              <tbody>
                {judgeScores.map(score => (
                  <tr key={score.id} className="bg-white border-b hover:bg-gray-50 last:border-none">
                    <th scope="row" className="px-4 py-3 font-medium text-gray-900">{score.id}</th>
                    <td className="px-4 py-3 text-center">{score.kg.toFixed(1)}</td>
                    <td className="px-4 py-3 text-center">{score.rag.toFixed(1)}</td>
                    <td className="px-4 py-3 text-center">{score.llm.toFixed(1)}</td>
                    <td className="px-4 py-3 text-center font-bold text-green-700 bg-green-50 rounded">{score.kgiqd.toFixed(1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </section>
  );
};

export default Result;

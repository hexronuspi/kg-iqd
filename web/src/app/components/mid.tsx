import Image from 'next/image';
import React from 'react';

const Mid = () => {
  const frameworkPath = "/kg-iqd/archKG.png";
  const datasetPath = "/kg-iqd/dataKG.png";

  return (
    <section className="bg-white font-sans text-gray-800 p-6 md:p-8 w-full">
      <div className="w-full max-w-6xl mx-auto space-y-16">

        {/* Section 1: KG-IQD Framework */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          
          <div className="w-full flex justify-center">
            <Image src={frameworkPath} alt={'framework'} unoptimized={true} width={500} height={500}/>
          </div>

          {/* Framework Description */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-gray-800">KG-IQD Framework</h3>
            
            <div>
              <strong className="font-semibold text-gray-700">KG-Guided Query Decomposition:</strong>
              <p className="text-gray-600 mt-1 text-sm leading-relaxed">
                KG-IQD first grounds the user query by retrieving relevant triples from our disaster-specific KG. This structured context provides a semantically rich prior that guides an LLM in decomposing the initial complex prompt into a series of focused, single-answer sub-queries.
              </p>
            </div>
            
            <div>
              <strong className="font-semibold text-gray-700">Targeted Retrieval & Synthesis:</strong>
              <p className="text-gray-600 mt-1 text-sm leading-relaxed">
                These sub-queries then drive a targeted RAG process that retrieves high-precision evidence from the raw text corpus. The final answer is synthesized by an LLM that integrates signals from both the retrieved textual context and the original KG grounding, enabling robust reasoning.
              </p>
            </div>
          </div>
        </div>

        {/* Section 2: Dataset */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          
          {/* Dataset Description (order-1 on small screens, order-2 on large) */}
          <div className="space-y-4 lg:order-2">
            <h3 className="text-2xl font-bold text-gray-800">Specialized Dataset</h3>
            <p className="text-gray-600 text-sm leading-relaxed">
              We curated specialized corpora from publicly available, reputable sources, including government assessments, NGO reports, and academic studies. The corpus collected contains details of the 2015 Nepal Earthquake and the 2018 Kerala Flood, each having 43 top level schema and 207 sub-level.
            </p>
          </div>

          {/* PDF Embed (order-2 on small screens, order-1 on large) */}
          <div className="w-full flex justify-center lg:order-1">
              <Image src={datasetPath} alt={'dataset'} unoptimized={true} width={500} height={500}/>
          </div>
        </div>

      </div>
    </section>
  );
};

export default Mid;
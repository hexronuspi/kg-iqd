import Link from 'next/link';
import React from 'react';

const authors = [
  { name: 'Aditya Raj', sup: '1', github: 'hexronuspi', linkedin: 'hexronus', email: 'adityar.ug22.ec@nitp.ac.in' },
  { name: 'Kuldeep Kurte', sup: '2', github: 'kuldeepkurte', linkedin: 'kuldeepkurte', email: 'kuldeep.kurte@iiit.ac.in' },
];

const affiliations = [
  { sup: '1', text: 'National Institute of Technology, Patna' },
  { sup: '2', text: 'IIIT Hyderabad' },
];

const socialIcons = {
  github: <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-6 h-6" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8Z" /></svg>,
  linkedin: <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6" aria-hidden="true"><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.25 6.5 1.75 1.75 0 016.5 8.25zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.67 1.67 0 0013 14.19a.29.29 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 4.42V19z" /></svg>,
  email: <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6" aria-hidden="true"><path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z" /><path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z" /></svg>,
};

const Title = () => (
  <section className="bg-white font-sans text-gray-800 p-8 md:p-12 w-full flex flex-col items-center text-center">
    <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 max-w-7xl">
      Knowledge Graph-Informed Query Decomposition(KG-IQD): Hybrid KG-RAG Reasoning in Noisy Context
    </h1>

    <div className="mt-8 flex flex-col md:flex-row justify-center items-center gap-8 md:gap-12">
      {authors.map(author => (
        <div key={author.name} className="flex flex-col items-center">
          <h2 className="text-xl md:text-2xl font-semibold">{author.name}<sup className="ml-1 text-sm font-medium">{author.sup}</sup></h2>
          <div className="mt-2 flex items-center space-x-4">
            <Link href={`https://github.com/${author.github}/`} target="_blank" rel="noopener noreferrer" aria-label={`${author.name}'s GitHub`} className="text-gray-500 hover:text-gray-900">{socialIcons.github}</Link>
            <Link href={`https://www.linkedin.com/in/${author.linkedin}`} target="_blank" rel="noopener noreferrer" aria-label={`${author.name}'s LinkedIn`} className="text-gray-500 hover:text-blue-600">{socialIcons.linkedin}</Link>
            <Link href={`mailto:${author.email}`} aria-label={`Email ${author.name}`} className="text-gray-500 hover:text-red-500">{socialIcons.email}</Link>
          </div>
        </div>
      ))}
    </div>

    <div className="text-left mt-8 pt-6 border-t border-gray-200 w-full max-w-2xl text-md text-gray-600 space-y-2">
      {affiliations.map(aff => <p key={aff.sup}><sup className="font-bold">{aff.sup}</sup>{aff.text}</p>)}
    </div>

    <div className="mt-12 w-full max-w-3xl text-left">
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-4">Abstract</h2>
        <p className="text-base text-gray-700 leading-relaxed text-justify">
            Disaster data is inherently noisy and heterogeneous, posing significant challenges for automated reasoning. 
            Retrieval-Augmented Generation (RAG) systems retrieve relevant documents but often fail to capture relational 
            structure, impairing tasks such as comparative analysis and summarization, critical for disaster response. 
            Knowledge graphs (KGs), while structured, are often sparse and lack contextual depth, which may not allow them 
            to capture in-depth information needed for reasoning and planning queries. We propose Knowledge Graph-Informed 
            Query Decomposition (KG-IQD), a hybrid KG-RAG framework that uses KGs to strategically guide the query 
            decomposition into a set of focused, single-answer, contextually relevant subqueries, which perform the 
            highly targeted RAG process, ensuring that the final LLM-generated answer is coherently grounded in both 
            the retrieved textual evidence and the rich structured context of the KG. We evaluated KG-IQD against strong 
            baselines using our novel Indian Disaster Dataset and an &quot;LLM-as-judge&quot; framework. To ensure a rigorous and 
            fair evaluation, our methodology mitigates positional bias through output randomization and employs a metric 
            that penalizes verbosity and irrelevance. The results demonstrate a clear advantage: KG-IQD outperforms RQ-RAG 
            by 14% and KG by 18%. Our dataset, code, and output are publicly available at: <Link href="https://github.com/hexronuspi/kg-iqd" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">github.com/hexronuspi/kg-iqd</Link>.
        </p>
    </div>

  </section>
);

export default Title;

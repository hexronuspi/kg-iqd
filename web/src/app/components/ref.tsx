import React from 'react';
import Link from 'next/link';

const referencesData = [
  {
    authors: 'K. Bollacker, C. Evans, P. Paritosh, T. Sturge, J. Taylor',
    title: 'Freebase: A collaboratively created graph database for structuring human knowledge,',
    publication: 'in: Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data, ACM, 2008, pp. 1247–1250.',
    doi: '10.1145/1376616.1376746',
  },
  {
    authors: 'P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W.-t. Yih, T. Rocktäschel, S. Riedel, D. Kiela',
    title: 'Retrieval-augmented generation for knowledge-intensive nlp tasks,',
    publication: 'in: Advances in Neural Information Processing Systems (NeurIPS), 2020.',
    url: 'https://arxiv.org/abs/2005.11401',
  },
  {
    authors: 'D. Edge, H. Trinh, N. Cheng, J. Bradley, A. Chao, A. Mody, S. Truitt, D. Metropolitansky, R. O. Ness, J. Larson',
    title: 'From local to global: A graph rag approach to query-focused summarization,',
    publication: 'arXiv preprint arXiv:2404.16130 (2024).',
    url: 'https://arxiv.org/abs/2404.16130',
  },
  {
    authors: 'S. Ji, S. Pan, E. Cambria, P. Marttinen, P. S. Yu',
    title: 'A survey on knowledge graphs: Representation, acquisition, and applications,',
    publication: 'IEEE Transactions on Neural Networks and Learning Systems 33 (2021) 494–514.',
    url: 'https://arxiv.org/abs/2002.00388',
  },
  {
    authors: 'T. Khot, H. Trivedi, M. Finlayson, Y. Fu, K. Richardson, P. Clark, A. Sabharwal',
    title: 'Decomposed prompting: A modular approach for solving complex tasks,',
    publication: 'in: International Conference on Learning Representations (ICLR), 2023.',
    url: 'https://arxiv.org/abs/2210.02406',
  },
  {
    authors: 'C.-M. Chan, C. Xu, R. Yuan, H. Luo, W. Xue, Y. Guo, J. Fu',
    title: 'Rq-rag: Learning to refine queries for retrieval-augmented generation,',
    publication: 'arXiv preprint arXiv:2404.00610 (2024).',
    url: 'https://arxiv.org/pdf/2404.00610',
  },
  {
    authors: 'L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, I. Stoica',
    title: 'Judging llm-as-a-judge with mt-bench and chatbot arena,',
    publication: 'arXiv preprint arXiv:2306.05685 (2023). NeurIPS 2023 Datasets and Benchmarks Track.',
    url: 'https://arxiv.org/abs/2306.05685',
    doi: '10.48550/arXiv.2306.05685',
  },
];

const Ref = () => {
  return (
    <section className="font-sans p-6 md:p-8 w-full">
      <div className="w-full max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">References</h2>
        <ol className="list-decimal list-inside space-y-4 text-sm text-gray-700">
          {referencesData.map((ref, index) => (
            <li key={index} className="pl-2 leading-relaxed">
              {ref.authors}, <em className="text-gray-800">{ref.title}</em> {ref.publication}
              {ref.url && (
                <Link href={ref.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline ml-1">
                  [URL]
                </Link>
              )}
              {ref.doi && (
                <Link href={`https://doi.org/${ref.doi}`} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline ml-1">
                  [DOI]
                </Link>
              )}
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
};

export default Ref;
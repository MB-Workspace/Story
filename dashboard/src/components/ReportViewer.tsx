'use client'

import { useState } from 'react'

const sampleReports = [
    { id: 1, title: 'Crypto Fraud Case 2024-001', date: '2024-03-15', status: 'completed' },
    { id: 2, title: 'Ransomware Payment Analysis', date: '2024-03-14', status: 'completed' },
    { id: 3, title: 'Shell Company Detection', date: '2024-03-13', status: 'pending' },
    { id: 4, title: 'Money Laundering Pattern', date: '2024-03-12', status: 'completed' },
]

export default function ReportViewer() {
    const [selectedReport, setSelectedReport] = useState<number | null>(1)

    const handleGenerateReport = () => {
        fetch('/api/vajra/reports/generate', { method: 'POST' })
            .then(res => res.json())
            .then(data => alert(`Report generated: ${data.report_id}`))
    }

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium">Forensic Reports</h3>
                <button
                    onClick={handleGenerateReport}
                    className="px-4 py-2 bg-primary text-white rounded hover:bg-blue-700"
                >
                    Generate New Report
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="border rounded">
                    <div className="p-4 border-b">
                        <h4 className="font-medium">Report List</h4>
                    </div>
                    <div className="divide-y">
                        {sampleReports.map(report => (
                            <div
                                key={report.id}
                                className={`p-4 cursor-pointer ${selectedReport === report.id ? 'bg-blue-50' : ''}`}
                                onClick={() => setSelectedReport(report.id)}
                            >
                                <div className="flex justify-between">
                                    <span className="font-medium">{report.title}</span>
                                    <span className={`px-2 py-1 text-xs rounded ${report.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                                        {report.status}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-500">{report.date}</p>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="border rounded">
                    <div className="p-4 border-b">
                        <h4 className="font-medium">Report Preview</h4>
                    </div>
                    <div className="p-4">
                        {selectedReport ? (
                            <div className="space-y-3">
                                <h5 className="font-medium">FORENSIC REPORT - CRYPTO-FRAUD-2024-001</h5>
                                <p className="text-sm">Generated: 2024-03-15 14:30:00</p>
                                <div className="bg-gray-50 p-3 rounded">
                                    <p className="text-sm">
                                        Analysis completed in 2.1s. Identified 12 entities with 3 threat matches.
                                        High-risk wallets detected: wallet_A, wallet_B.
                                    </p>
                                </div>
                                <button className="px-3 py-1 text-sm border rounded hover:bg-gray-50">
                                    Download PDF
                                </button>
                            </div>
                        ) : (
                            <p className="text-gray-500">Select a report to preview</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
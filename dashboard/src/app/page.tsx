'use client'

import { useState, useEffect } from 'react'
import EntityGraph from '@/components/EntityGraph'
import ThreatMetrics from '@/components/ThreatMetrics'
import ReportViewer from '@/components/ReportViewer'
import WalletSearch from '@/components/WalletSearch'

export default function Home() {
    const [activeTab, setActiveTab] = useState('dashboard')
    const [caseData, setCaseData] = useState(null)

    useEffect(() => {
        // Fetch initial case data
        fetch('/api/vajra/cases/current')
            .then(res => res.json())
            .then(data => setCaseData(data))
            .catch(err => console.error('Failed to fetch case data:', err))
    }, [])

    return (
        <div className="space-y-6">
            <div className="flex space-x-4 border-b">
                <button
                    className={`px-4 py-2 ${activeTab === 'dashboard' ? 'border-b-2 border-primary text-primary' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('dashboard')}
                >
                    Dashboard
                </button>
                <button
                    className={`px-4 py-2 ${activeTab === 'graph' ? 'border-b-2 border-primary text-primary' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('graph')}
                >
                    Entity Graph
                </button>
                <button
                    className={`px-4 py-2 ${activeTab === 'threats' ? 'border-b-2 border-primary text-primary' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('threats')}
                >
                    Threat Analysis
                </button>
                <button
                    className={`px-4 py-2 ${activeTab === 'reports' ? 'border-b-2 border-primary text-primary' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('reports')}
                >
                    Reports
                </button>
            </div>

            <div className="mb-6">
                <WalletSearch />
            </div>

            {activeTab === 'dashboard' && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                        <h2 className="text-xl font-semibold mb-4">Case Overview</h2>
                        {caseData ? (
                            <div className="space-y-2">
                                <p><strong>Case ID:</strong> {caseData.case_id}</p>
                                <p><strong>Entities:</strong> {caseData.entity_count}</p>
                                <p><strong>Threat Matches:</strong> {caseData.threat_count}</p>
                                <p><strong>Processing Time:</strong> {caseData.processing_time}s</p>
                            </div>
                        ) : (
                            <p>Loading case data...</p>
                        )}
                    </div>
                    <div className="bg-white rounded-lg shadow p-6">
                        <ThreatMetrics />
                    </div>
                </div>
            )}

            {activeTab === 'graph' && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-semibold mb-4">Entity Graph Visualization</h2>
                    <EntityGraph />
                </div>
            )}

            {activeTab === 'threats' && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-semibold mb-4">Threat Analysis</h2>
                    <div className="space-y-4">
                        <div className="p-4 bg-red-50 border border-red-200 rounded">
                            <h3 className="font-semibold text-red-700">High-Risk Threats</h3>
                            <p className="text-sm text-red-600">Lazarus Group detected with 92% confidence</p>
                        </div>
                        <div className="p-4 bg-yellow-50 border border-yellow-200 rounded">
                            <h3 className="font-semibold text-yellow-700">Medium-Risk Threats</h3>
                            <p className="text-sm text-yellow-600">APT29 detected with 87% confidence</p>
                        </div>
                    </div>
                </div>
            )}

            {activeTab === 'reports' && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-semibold mb-4">Forensic Reports</h2>
                    <ReportViewer />
                </div>
            )}
        </div>
    )
}
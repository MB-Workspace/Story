'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const threatData = [
    { day: 'Mon', threats: 4, anomalies: 2 },
    { day: 'Tue', threats: 7, anomalies: 3 },
    { day: 'Wed', threats: 5, anomalies: 4 },
    { day: 'Thu', threats: 8, anomalies: 5 },
    { day: 'Fri', threats: 6, anomalies: 3 },
    { day: 'Sat', threats: 3, anomalies: 1 },
    { day: 'Sun', threats: 2, anomalies: 0 },
]

export default function ThreatMetrics() {
    return (
        <div>
            <h3 className="text-lg font-medium mb-4">Threat Detection Trends</h3>
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={threatData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="day" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="threats" stroke="#3b82f6" activeDot={{ r: 8 }} />
                        <Line type="monotone" dataKey="anomalies" stroke="#ef4444" />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-4">
                <div className="bg-blue-50 p-3 rounded">
                    <p className="text-sm text-blue-700">Total Threats Detected</p>
                    <p className="text-2xl font-bold text-blue-900">35</p>
                </div>
                <div className="bg-red-50 p-3 rounded">
                    <p className="text-sm text-red-700">Benford Anomalies</p>
                    <p className="text-2xl font-bold text-red-900">18</p>
                </div>
            </div>
        </div>
    )
}
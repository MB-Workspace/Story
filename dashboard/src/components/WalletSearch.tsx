'use client'

import { useState } from 'react'

export default function WalletSearch() {
    const [address, setAddress] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<any>(null)

    const handleSearch = async () => {
        if (!address.trim()) return

        setLoading(true)
        try {
            const response = await fetch(`/api/vajra/wallet/${address}`)
            const data = await response.json()
            setResult(data)
        } catch (error) {
            console.error('Search failed:', error)
            setResult({ error: 'Failed to fetch wallet data' })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="space-y-4">
            <div className="flex space-x-2">
                <input
                    type="text"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    placeholder="Enter wallet address (0x...)"
                    className="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
                />
                <button
                    onClick={handleSearch}
                    disabled={loading}
                    className="px-6 py-2 bg-primary text-white rounded hover:bg-blue-700 disabled:opacity-50"
                >
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </div>

            {result && (
                <div className="bg-white border rounded p-4">
                    {result.error ? (
                        <p className="text-red-600">{result.error}</p>
                    ) : (
                        <div className="space-y-3">
                            <h4 className="font-medium">Wallet Analysis</h4>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="text-sm text-gray-500">Address</p>
                                    <p className="font-mono text-sm truncate">{result.address}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500">Risk Score</p>
                                    <p className={`text-lg font-bold ${result.risk_score > 70 ? 'text-red-600' : result.risk_score > 40 ? 'text-yellow-600' : 'text-green-600'}`}>
                                        {result.risk_score}/100
                                    </p>
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500">Transactions</p>
                                    <p className="text-lg">{result.tx_count}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500">Balance</p>
                                    <p className="text-lg">{result.balance_usd?.toFixed(2)} USD</p>
                                </div>
                            </div>
                            {result.threat_matches && result.threat_matches.length > 0 && (
                                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded">
                                    <p className="text-sm font-medium text-red-800">Threat Matches</p>
                                    <ul className="mt-1 space-y-1">
                                        {result.threat_matches.map((match: any, idx: number) => (
                                            <li key={idx} className="text-sm text-red-700">
                                                {match.threat} ({match.confidence * 100}% confidence)
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
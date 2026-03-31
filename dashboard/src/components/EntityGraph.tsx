'use client'

import { useEffect, useRef } from 'react'
import ForceGraph2D from 'react-force-graph-2d'

export default function EntityGraph() {
    const graphRef = useRef<any>(null)
    const [graphData, setGraphData] = useState<any>(null)

    useEffect(() => {
        // Fetch graph data from API
        fetch('/api/vajra/graph')
            .then(res => res.json())
            .then(data => {
                const nodes = Object.keys(data.entities).map(id => ({ id, label: id }))
                const links = []
                for (const [source, connections] of Object.entries(data.entities)) {
                    for (const target of connections) {
                        links.push({ source, target })
                    }
                }
                setGraphData({ nodes, links })
            })
    }, [])

    if (!graphData) {
        return <div className="h-96 flex items-center justify-center">Loading graph...</div>
    }

    return (
        <div className="h-96 border rounded">
            <ForceGraph2D
                ref={graphRef}
                graphData={graphData}
                nodeLabel="id"
                nodeColor={() => '#3b82f6'}
                linkColor={() => '#9ca3af'}
                backgroundColor="#ffffff"
            />
        </div>
    )
}

function useState<T>(initialState: T): [T, (value: T) => void] {
    const [state, setState] = React.useState(initialState)
    return [state, setState]
}

import React from 'react'
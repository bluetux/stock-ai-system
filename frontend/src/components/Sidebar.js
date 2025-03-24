// 📁 frontend/src/components/Sidebar.js

import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const Sidebar = () => {
    const [groups, setGroups] = useState({});

    useEffect(() => {
        axios.get("/api/groups")
            .then((res) => {
                console.log("Sidebar API Response:", res.data);  // 👈 요 줄 추가
                setGroups(res.data);
            })
            .catch((err) => console.error("Sidebar fetch error:", err));
    }, []);

    return (
        <div className="w-64 bg-gray-800 text-white h-screen p-4 overflow-y-auto">
            {Object.entries(groups).map(([region, groupMap]) => (
                <div key={region} className="mb-4">
                    <h2 className="text-blue-300 font-bold mb-1">{region}</h2>
                    {Object.entries(groupMap).map(([group, stocks]) => (
                        <div key={group} className="ml-4">
                            <h3 className="text-blue-200">{group}</h3>
                            <ul className="ml-2 text-white">
                                {stocks.map((stock, index) => (
                                    <li key={index}>
                                        <Link to={`/dashboard/stocks/${stock.ticker}`} className="hover:underline">
                                            {stock.alias}
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            ))}


        </div>
    );
};

export default Sidebar;

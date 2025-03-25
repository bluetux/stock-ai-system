import React from "react";
import { Settings, ListChecks } from "lucide-react";
import { NavLink } from "react-router-dom";

const SettingsSidebar = () => {
    return (
        <div className="w-52 min-h-screen bg-gray-800 text-white p-4 border-r border-gray-300">
            <h2 className="text-xl font-bold mb-6 flex items-center">
                <Settings className="w-5 h-5 mr-2" />
                설정 메뉴
            </h2>

            <nav className="flex flex-col space-y-3">
                <NavLink
                    to="/dashboard/settings/watchlist"
                    className={({ isActive }) =>
                        `flex items-center gap-2 px-2 py-2 rounded hover:bg-gray-700 text-white ${isActive ? "bg-gray-700 font-bold" : ""
                        }`
                    }
                >
                    <ListChecks className="w-4 h-4" />
                    관심 종목 설정
                </NavLink>

                <NavLink
                    to="/dashboard/settings/groups"
                    className={({ isActive }) =>
                        `flex items-center gap-2 px-2 py-2 rounded hover:bg-gray-700 text-white ${isActive ? "bg-gray-700 font-bold" : ""
                        }`
                    }
                >
                    <ListChecks className="w-4 h-4" />
                    그룹 설정
                </NavLink>
            </nav>
        </div>
    );
};

export default SettingsSidebar;
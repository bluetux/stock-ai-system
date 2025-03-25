// src/layouts/SettingsLayout.jsx
import { Outlet } from "react-router-dom";
import SettingsSidebar from "./SettingsSidebar";

const SettingsLayout = () => {
    return (
        <div className="flex bg-settings min-h-screen">
            <SettingsSidebar />
            <div className="flex-1 p-6">
                <Outlet />
            </div>
        </div>
    );
};

export default SettingsLayout;
// 📁 src/pages/settings/GroupSettingsPage.jsx
import React, { useEffect, useState } from "react";
import { ListIcon, Trash2, Plus } from "lucide-react";

const GroupSettingsPage = () => {
  const [groups, setGroups] = useState([]);
  const [selected, setSelected] = useState(null);
  const [editGroup, setEditGroup] = useState({
    name: "",
    region: "한국",
    icon: "",
    stocks: [],
  });

  useEffect(() => {
    fetch("/api/groups/")
      .then((res) => res.json())
      .then((data) => {
        const flatGroups = [];
        for (const region in data) {
          for (const groupId in data[region]) {
            flatGroups.push({
              id: parseInt(groupId),
              name: data[region][groupId].name,
              region,
              icon: data[region][groupId].icon || "",
              stocks: data[region][groupId].stocks || [],
            });
          }
        }
        setGroups(flatGroups);
      });
  }, []);

  const handleSelect = (group) => {
    if (selected?.id === group.id) {
      setSelected(null);
    } else {
      setSelected(group);
      setEditGroup({
        ...group,
        stocks: group.stocks || [],
      });
    }
  };

  const handleInputChange = (field, value) => {
    setEditGroup((prev) => ({ ...prev, [field]: value }));
  };

  const handleCancel = () => setSelected(null);

  const handleDeleteStock = (ticker) => {
    if (confirm(`${ticker} 종목을 이 그룹에서 삭제할까요?`)) {
      setEditGroup((prev) => ({
        ...prev,
        stocks: prev.stocks.filter((s) => s.ticker !== ticker),
      }));
    }
  };

  const handleSave = () => {
    alert(`그룹 저장: ${editGroup.name}`);
    setSelected(null);
  };

  const handleAddGroup = () => {
    setSelected({ id: null }); // 새 그룹은 id 없음
    setEditGroup({
      name: "",
      region: "한국",
      icon: "",
      stocks: [],
    });
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold flex items-center mb-2">
        <ListIcon className="w-5 h-5 mr-2" />
        그룹 관리
      </h2>
      <p className="mb-4 text-gray-600">그룹을 추가/수정하고 그룹에 종목을 연결하거나 제거할 수 있습니다.</p>

      <div className="flex items-center gap-4 mb-4">
        <button
          onClick={handleAddGroup}
          className="flex items-center px-3 py-2 bg-black text-white rounded hover:bg-gray-800"
        >
          <Plus className="w-4 h-4 mr-1" />
          그룹 추가
        </button>
      </div>

      <div className="space-y-2">
        {groups.map((group) => (
          <div key={group.id}>
            <div
              className="p-3 bg-white border rounded cursor-pointer flex justify-between items-center hover:bg-gray-50"
              onClick={() => handleSelect(group)}
            >
              <div>
                <div className="font-semibold">{group.name}</div>
                <div className="text-sm text-gray-500">
                  {group.region} / {group.icon || "아이콘 없음"}
                </div>
              </div>
            </div>

            {selected?.id === group.id && (
              <div className="p-4 mt-2 mb-4 border bg-gray-50 rounded">
                <h3 className="text-lg font-semibold mb-4">
                  {editGroup.name || "새 그룹"} 정보 수정
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div>
                    <label className="text-sm font-medium">그룹 이름</label>
                    <input
                      value={editGroup.name}
                      onChange={(e) => handleInputChange("name", e.target.value)}
                      className="w-full border px-3 py-2 rounded mt-1"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">지역</label>
                    <select
                      value={editGroup.region}
                      onChange={(e) => handleInputChange("region", e.target.value)}
                      className="w-full border px-3 py-2 rounded mt-1"
                    >
                      <option>한국</option>
                      <option>미국</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium">아이콘</label>
                    <input
                      value={editGroup.icon}
                      onChange={(e) => handleInputChange("icon", e.target.value)}
                      className="w-full border px-3 py-2 rounded mt-1"
                      placeholder="activity, chip, globe 등"
                    />
                  </div>
                </div>

                <div className="mt-4">
                  <label className="text-sm font-medium">등록된 종목</label>
                  <ul className="mt-2 space-y-2">
                    {editGroup.stocks.length === 0 && (
                      <li className="text-sm text-gray-400">등록된 종목 없음</li>
                    )}
                    {editGroup.stocks.map((stock) => (
                      <li
                        key={stock.ticker}
                        className="flex justify-between items-center border px-3 py-2 rounded bg-white"
                      >
                        <div>
                          <div className="font-medium">{stock.alias}</div>
                          <div className="text-sm text-gray-500">{stock.ticker}</div>
                        </div>
                        <button
                          onClick={() => handleDeleteStock(stock.ticker)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mt-4 flex justify-end space-x-2">
                  <button
                    onClick={handleCancel}
                    className="px-4 py-2 border rounded hover:bg-gray-100"
                  >
                    취소
                  </button>
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
                  >
                    저장
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default GroupSettingsPage;
import { useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

export default function DataSpikes() {
  const count = 160;

  const spikes = useMemo(() => {
    const tmp = [];
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const radius = 2.3;

      tmp.push([
        Math.cos(angle) * radius,
        Math.sin(angle) * radius,
      ]);
    }
    return tmp;
  }, []);

  return (
    <group rotation={[Math.PI / 2, 0, 0]}>
      {spikes.map(([x, y], i) => (
        <mesh key={i} position={[x, y, 0]}>
          <cylinderGeometry args={[0.015, 0.015, 0.5, 8]} />
          <meshBasicMaterial
            color="#11cfff"
            transparent
            opacity={0.7}
          />
        </mesh>
      ))}
    </group>
  );
}

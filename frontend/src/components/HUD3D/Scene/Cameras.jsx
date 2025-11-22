import { useThree, useFrame } from "@react-three/fiber";

export default function Cameras() {
  const { camera } = useThree();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();

    camera.position.x = Math.sin(t * 0.2) * 0.15;
    camera.position.y = 2.5 + Math.sin(t * 0.1) * 0.1;

    camera.lookAt(0, 0, 0);
  });

  return null;
}

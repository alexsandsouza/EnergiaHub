import { test, expect } from '@playwright/test';
test('navigation and experimental workflows', async ({page})=>{
 await page.route('https://**/*',r=>r.abort());
 await page.goto('http://127.0.0.1:8765/');
 const nav=async id=>{await page.locator('[data-page="'+id+'"]').click();await expect(page.locator('section#'+id)).toBeVisible()};
 await nav('lab');await page.locator('#labStart').click();await expect(page.locator('#labCount')).not.toHaveText('0');await page.locator('#labStop').click();
 await nav('timeseries');await expect(page.locator('#tsStats')).toContainText('Média:');
 await nav('iot');await page.locator('#iotSubscribe').click();await page.locator('#iotPublish').click();await expect(page.locator('#iotStatus')).toContainText('1 entregas');
 await nav('twin');await page.locator('#twinStart').click();await expect(page.locator('#twinState')).toHaveText('Ativo');
 await nav('events');await expect(page.locator('#evList')).toContainText('Entidade virtual');
 await nav('research');await page.locator('#resHyp').fill('Comparar dispersão');await page.locator('#resRun').click();await expect(page.locator('#resResult')).toContainText('smoothed');
});
